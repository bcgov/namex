import sys

from sqlalchemy import text
from datetime import datetime, timedelta

from flask import Flask, g, current_app

from namex import db
from namex.models import Request, State, User, Event
from namex.services import EventRecorder
from namex.utils.logging import setup_logging

from config import Config

setup_logging() ## important to do this first


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    app.app_context().push()
    current_app.logger.debug('created the Flask App and pushed the App Context')

    return app


app = create_app(Config)
start_time = datetime.utcnow()
row_count = 0

try:
    sql = "select id,synonyms_text " \
          "from synonym " \
          "where synonyms_text~'\w\s\w'"

    reqs = db.session.execute(sql)

    multi_word_syns = []
    for r in reqs:
        current_app.logger.debug('processing id: {}'.format(r.id))

        # create a list of all the synonyms for this row
        synonyms = [word.strip() for word in r.synonyms_text.split(',')]
        new_syn_text = ''
        update_row = False
        for synonym in synonyms:

            if ' ' in synonym:
                updated_synonym = synonym.replace(' ','')
                multi_word_syns.append((synonym, updated_synonym))
                update_row = True
                new_syn_text += updated_synonym + ','
            else:
                new_syn_text += synonym + ','

        if update_row:
            update_sql = "update synonym " \
                         "set synonyms_text = \'{text}\' " \
                         "where id={id}".format(text=new_syn_text[:-1], id=r.id)
            db.session.execute(update_sql)
            db.session.commit()
            row_count += 1

    # add new multi word synonyms to multi_word_syns.txt and protected-multi.txt
    if len(multi_word_syns) > 0:
        old_multi_word_syns = open('solr-synonym-updater/multi_word_syns.txt').read()
        old_protected_syns = open('solr-synonym-updater/protected_syns.txt').read()

        for syn_tuple in multi_word_syns:
            multi_syn = syn_tuple[0]
            squished_multi_syn = syn_tuple[1]

            if multi_syn in old_multi_word_syns:
                pass
            else:
                open('solr-synonym-updater/multi_word_syns.txt', 'a+').write('\n' + multi_syn + '=>' + squished_multi_syn)
                open('solr-synonym-updater/protected_syns.txt', 'a+').write(squished_multi_syn + ',')


except Exception as err:
    db.session.rollback()
    print('Failed to update multi-synonyms: ', err, err.with_traceback(None), file=sys.stderr)
    exit(1)

app.do_teardown_appcontext()
end_time = datetime.utcnow()
print("job - columns updated: {0} completed in:{1}".format(row_count, end_time-start_time))
exit(0)
