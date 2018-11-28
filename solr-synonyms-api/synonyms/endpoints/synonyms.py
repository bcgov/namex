
import logging

import flask_restplus

import synonyms.models.synonym as synonym


__all__ = ['api']


api = flask_restplus.Namespace('Synonyms', description='Work with synonyms used in Solr')


@api.route('/<term>', methods=['GET'])
class _Synonyms(flask_restplus.Resource):
    @staticmethod
    def get(term):
        term = term.strip()
        logging.debug('Doing synonym search for "{}"'.format(term))

        results = synonym.Synonym.find(term)

        if not results:
            return {'message': 'Term \'{}\' not found in any synonyms list'.format(term)}, 404

        response_list = []
        for result in results:
            response_list.append(result.synonyms_text)

        return ('results', response_list), 200
