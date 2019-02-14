
import logging

import flask_restplus

import synonyms.models.synonym as synonym


__all__ = ['api']


api = flask_restplus.Namespace('Synonyms', description='Work with synonyms used in Solr')


@api.route('/<col>/<term>', methods=['GET'])
class _Synonyms(flask_restplus.Resource):
    @staticmethod
    def get(col, term):
        term = term.strip().lower()
        logging.debug('Doing {} search for "{}"'.format(col, term))

        results = synonym.Synonym.find(term, col)

        if not results:
            return {'message': 'Term \'{}\' not found in any synonyms list'.format(term)}, 404

        response_list = []
        for result in results:
            if col == 'synonyms_text':
                response_list.append(result.synonyms_text)
            # col == stems_text
            else:
                response_list.append(result.stems_text)
        print(response_list)
        return ('results', response_list), 200
