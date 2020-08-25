import sys, os
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

setup_logging()  ## important to do this first

entry_params = {
    'entity_type': 'CR',
}


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    app.app_context().push()
    current_app.logger.debug('created the Flask App and pushed the App Context')

    return app


def name_profile_data(request_id, nr_num, state, choice, name, decision_text, conflict1_num, conflict1):
    name_profile = {'id': request_id,
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


def name_response_data(payload):
    name_response = {'result_state': 'NULL',
                     'result_decision_text': 'NULL',
                     'result_conflict_num1': 'NULL',
                     'result_conflict1': 'NULL',
                     'result_response': 'NULL'
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
        else:
            name_response['result_state'] = 'NULL'

    name_response['result_decision_text'] = decision_text
    name_response['result_response'] = payload.to_json()

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
              "r.request_type_cd = " + '\'' + EntityTypes.CORPORATION.value + '\'' + " and " \
              "r.nr_num not in (select nr_num from uat_results) " \
              "order by r.submitted_date " \
              "limit " + MAX_ROW_LIMIT

        requests = db.session.execute(sql)
        for request_id, nr_num, state_cd, choice, name, decision_text, conflict1_num, conflict1, conflict_num1 in requests:
            if entry_params['entity_type'] in BCProtectedNameEntityTypes.list():
                service = ProtectedNameAnalysisService()
                builder = NameAnalysisBuilder(service)

                service.use_builder(builder)
                service.set_entity_type(entry_params.get('entity_type'))
                service.set_name(name)

                analysis = service.execute_analysis()

                # Build the appropriate response for the analysis result
                analysis_response = AnalysisResponse(service, analysis)
                payload = analysis_response.build_response()

                profile_data = name_profile_data(request_id, nr_num, state_cd, choice, name, decision_text,
                                                 conflict1_num, conflict1)
                response_data = name_response_data(payload)

                data_dict = profile_data.copy()
                data_dict.update(response_data)

            cols = data_dict.keys()
            cols_str = ','.join(cols)
            record_to_insert = tuple([data_dict[k] for k in cols])

            db.session.execute('insert into uat_results VALUES {};'.format(record_to_insert))
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
