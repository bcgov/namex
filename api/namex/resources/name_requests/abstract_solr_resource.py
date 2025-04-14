import pysolr

from flask import current_app
from flask_restx import Resource

from namex.models import State

from namex.services.name_request.exceptions import SolrUpdateError


class AbstractSolrResource(Resource):
    """
    Abstract class. Extended by AbstractNameRequestResource.
    Avoid using this class elsewhere, please use AbstractNameRequestResource instead.
    """
    @classmethod
    def create_solr_nr_doc(cls, solr_core, name_request):
        try:
            # Create a new solr doc
            solr_name = name_request.names[0].name
            solr_docs = []
            nr_doc = {
                'id': name_request.nrNum,
                'name': solr_name,
                'source': 'NR',
                'start_date': name_request.submittedDate.strftime('%Y-%m-%dT%H:%M:00Z')
            }

            solr_docs.append(nr_doc)
            cls.add_solr_doc(solr_core, solr_docs)

        except Exception as err:
            raise SolrUpdateError(err)

    @classmethod
    def add_solr_doc(cls, solr_core, solr_docs):
        try:
            SOLR_API_URL = f'{current_app.config.get("SOLR_BASE_URL")}/solr/'
            solr = pysolr.Solr(SOLR_API_URL + solr_core + '/', timeout=10)
            result = solr.add(solr_docs, commit=True)
        except Exception as err:
            raise SolrUpdateError(err)

        return result

    @classmethod
    def delete_solr_doc(cls, solr_core, doc_id):
        try:
            SOLR_API_URL = f'{current_app.config.get("SOLR_BASE_URL")}/solr/'
            solr = pysolr.Solr(SOLR_API_URL + solr_core + '/', timeout=10)
            result = solr.delete(id=doc_id, commit=True)

        except Exception as err:
            raise SolrUpdateError(err)

        return result

    @classmethod
    def update_solr_service(cls, nr_model, temp_nr_num=None):
        SOLR_CORE = 'possible.conflicts'

        if current_app.config.get('DISABLE_NAMEREQUEST_SOLR_UPDATES', 0) == 1:
            # Ignore update to SOLR if SOLR updates [DISABLE_NAMEREQUEST_SOLR_UPDATES] are explicitly disabled in your .env
            return

        # Only update solr for corp entity types
        # TODO: Use the actual codes from the constants file...
        if nr_model.stateCd in [State.COND_RESERVE, State.RESERVED, State.CONDITIONAL, State.APPROVED, State.CANCELLED] and \
                nr_model.entity_type_cd in ['CR', 'UL', 'BC', 'CP', 'PA', 'XCR', 'XUL', 'XCP', 'CC', 'FI', 'XCR', 'XUL', 'XCP']:

            cls.create_solr_nr_doc(SOLR_CORE, nr_model)
            if temp_nr_num:
                # This performs a safe delete, we check to see if the temp ID exists before deleting
                cls.delete_solr_doc(SOLR_CORE, temp_nr_num)

    @staticmethod
    def log_error(msg, err):
        return msg.format(err)
