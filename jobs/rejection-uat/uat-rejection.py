import sys, os, re
from datetime import datetime

from flask import Flask, g, current_app
from namex import db
from namex.constants import BCProtectedNameEntityTypes, EntityTypes
from namex.models.state import State
from namex.services.name_request.auto_analyse import AnalysisIssueCodes
from namex.services.name_request.auto_analyse.protected_name_analysis import ProtectedNameAnalysisService
from namex.services.name_request.builders.name_analysis_builder import NameAnalysisBuilder
from namex.resources.auto_analyse.paths.bc_name_analysis.bc_name_analysis_response import \
    BcAnalysisResponse as AnalysisResponse
from namex.utils.logging import setup_logging
from config import Config
from sqlalchemy import Column

setup_logging()  ## important to do this first

entry_params = {
    'entity_type': 'CR',
}


class UatResults(db.Model):
    __tablename__ = 'uat_results'

    id = Column(db.Integer, primary_key=True, autoincrement=True)

    nr_num = Column(db.VARCHAR(10))
    nr_state = Column(db.VARCHAR(20))
    choice = Column(db.Integer)
    name = Column(db.VARCHAR(1024))
    name_state = db.Column(db.VARCHAR(20))
    decision_text = db.Column(db.VARCHAR(1024))
    conflict_num1 = db.Column(db.VARCHAR(20))
    conflict1 = db.Column(db.VARCHAR(1024))
    result_state = Column(db.VARCHAR(20))
    result_decision_text = db.Column(db.VARCHAR(2048))
    result_conflict_num1 = Column(db.VARCHAR(20))
    result_conflict1 = db.Column(db.VARCHAR(1024))
    result_response = db.Column(db.JSON)
    result_duration_secs = Column(db.Integer)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def save_to_session(self):
        db.session.add(self)


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    app.app_context().push()
    current_app.logger.debug('created the Flask App and pushed the App Context')

    return app


def name_profile_data(nr_num, state, choice, name, decision_text, conflict1_num, conflict1):
    seq_id = db.session.execute("select nextval('uat_results_seq') as id").fetchone()
    name_profile = {'id': seq_id[0],
                    'nr_num': nr_num,
                    'nr_state': state,
                    'choice': choice,
                    'name': name,
                    'name_state': State.REJECTED,
                    'decision_text': decision_text,
                    'conflict_num1': conflict1_num,
                    'conflict1': conflict1
                    }

    return name_profile


def name_response_data(payload, duration):
    name_response = {'result_state': None,
                     'result_decision_text': None,
                     'result_conflict_num1': None,
                     'result_conflict1': None,
                     'result_response': None,
                     'result_duration_secs': None
                     }

    decision_text = ''
    for element in payload.issues:
        decision_text += 'issue_type: ' + element.issue_type + '. Line1: ' + element.line1 + '. '

        if element.issue_type in (AnalysisIssueCodes.CORPORATE_CONFLICT, AnalysisIssueCodes.QUEUE_CONFLICT):
            for conflict in element.conflicts:
                name_response['result_conflict_num1'] = conflict.id
                name_response['result_conflict1'] = conflict.name

        elif element.issue_type in (AnalysisIssueCodes.ADD_DISTINCTIVE_WORD, AnalysisIssueCodes.ADD_DESCRIPTIVE_WORD,
                                    AnalysisIssueCodes.WORDS_TO_AVOID, AnalysisIssueCodes.TOO_MANY_WORDS):
            name_response['result_state'] = State.REJECTED

    if not payload.issues:
        name_response['result_state'] = State.APPROVED

    name_response['result_decision_text'] = decision_text
    name_response['result_response'] = payload.to_json()
    name_response['result_duration_secs'] = duration.seconds

    return name_response


if __name__ == "__main__":
    app = create_app(Config)
    start_time = datetime.utcnow()
    row_count = 0
    MAX_ROW_LIMIT = os.getenv('MAX_ROWS', '100')

    try:

        sql = "select r.id, r.nr_num, r.state_cd, n.choice, n.name, n.decision_text, n.conflict1_num, n.conflict1, n.conflict1_num " \
              "from requests r, names n " \
              "where r.id = n.nr_id and n.state = " + '\'' + State.REJECTED + '\'' + " and " \
              "r.state_cd in(" + '\'' + State.APPROVED + '\',' + '\'' + State.CONDITIONAL + '\',' + '\'' + State.REJECTED + '\') and '\
              "r.request_type_cd = " + '\'' + EntityTypes.CORPORATION.value + '\'' + " and " \
              "r.nr_num not in (select nr_num from uat_results) " \
              "order by r.submitted_date " \
              "limit " + MAX_ROW_LIMIT

        requests = db.session.execute(sql)
        for request_id, nr_num, state_cd, choice, name, decision_text, conflict1_num, conflict1, conflict_num1 in requests:
            if entry_params['entity_type'] in BCProtectedNameEntityTypes.list():
                start_time_name = datetime.utcnow()
                service = ProtectedNameAnalysisService()
                builder = NameAnalysisBuilder(service)

                service.use_builder(builder)
                service.set_entity_type(entry_params.get('entity_type'))
                service.set_name(name)

                analysis = service.execute_analysis()

                # Build the appropriate response for the analysis result
                analysis_response = AnalysisResponse(service, analysis)
                payload = analysis_response.build_response()
                end_time_name = datetime.utcnow()

                profile_data = name_profile_data(nr_num, state_cd, choice, name, decision_text,
                                                 conflict1_num, conflict1)
                response_data = name_response_data(payload, duration=end_time_name - start_time_name)

                data_dict = profile_data.copy()
                data_dict.update(response_data)

                uat = UatResults()
                uat.id = data_dict['id']
                uat.nr_num = data_dict['nr_num']
                uat.nr_state = data_dict['nr_state']
                uat.choice = data_dict['choice']
                uat.name = data_dict['name']
                uat.name_state = data_dict['name_state']
                uat.decision_text = data_dict['decision_text']
                uat.conflict_num1 = data_dict['conflict_num1']
                uat.conflict1 = data_dict['conflict1']
                uat.result_state = data_dict['result_state']
                uat.result_decision_text = data_dict['result_decision_text']
                uat.result_conflict_num1 = data_dict['result_conflict_num1']
                uat.result_conflict1 = data_dict['result_conflict1']
                uat.result_response = data_dict['result_response']
                uat.result_duration_secs = data_dict['result_duration_secs']

                db.session.add(uat)
                db.session.commit()
                row_count += 1

    except Exception as err:
        db.session.rollback()
        print('Failed to update events: ', err, err.with_traceback(None), file=sys.stderr)
        exit(1)

    app.do_teardown_appcontext()
    end_time = datetime.utcnow()
    print("job - columns updated: {0} completed in:{1}".format(row_count, end_time - start_time))
    exit(0)
