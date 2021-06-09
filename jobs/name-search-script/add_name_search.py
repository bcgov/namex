"""Script for updating nameSearch column (to be run once after column is added)."""
from flask import Flask, current_app

from namex import db
from namex.models import Request
from namex.utils.logging import setup_logging

from config import Config


setup_logging()  # important to do this first


def create_app(config=Config) -> Flask:
    """Create instance of app."""
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    app.app_context().push()
    current_app.logger.debug('created the Flask App and pushed the App Context')

    return app


def get_ops_params() -> int:
    """Get params for job."""
    max_rows = int(current_app.config.get('MAX_ROW_LIMIT', 500))

    return max_rows


def add_names_to_name_search(total_count):
    """Loop through all NRs with null nameSearch anf update them."""
    max_rows = get_ops_params()
    row_count = 0

    try:
        nrs_for_update = db.session.query(Request). \
            filter(Request.nameSearch == None). \
            order_by(Request.submittedDate.desc()). \
            limit(max_rows).all()

        for nr in nrs_for_update:
            row_count += 1
            current_app.logger.debug(f'processing: {nr.nrNum}, count: {row_count}, previous batch total {total_count}')
            names = nr.names.all()
            # format the names into a string like: |1<name1>|2<name2>|3<name3>
            name_search = ''
            for name, index in zip(names, range(len(names))):
                name_search += f'|{index + 1}{name.name}{index + 1}|'
            # update the name_search field of the nr with the formatted string
            nr.nameSearch = name_search
            db.session.add(nr)

        db.session.commit()
        return row_count, True

    except Exception as err:
        current_app.logger.error(err)
        db.session.rollback()
        return -1, False


if __name__ == '__main__':
    app = create_app(Config)
    total_count = 0
    count = -1
    success = True
    while count != 0 and success:
        count, success = add_names_to_name_search(total_count)
        if success:
            total_count += count
        current_app.logger.debug(f'batch processed {count} NRs. Total processed: {total_count}')
