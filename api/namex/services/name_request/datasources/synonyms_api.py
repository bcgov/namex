import os
from .abstract_api_client import AbstractApiClient, ApiError

# Must be running the synonyms API
SYNONYMS_API_BASE_URL = os.getenv('SOLR_SYNONYMS_API_URL')

'''
eg:
http://localhost:5555/api/v1/synonyms/category/scuba
'''


class SynonymsApi(AbstractApiClient):
    _base_uri = SYNONYMS_API_BASE_URL

    '''
    async api
    '''

    @classmethod
    async def get_synonyms_async(cls, on_success=None, on_error=None):
        resp = await cls.get_async('/category/scuba')
        if resp.status_code != 200:
            raise ApiError('GET /synonyms/ {}'.format(resp.status_code))

        if resp.status_code == 200:
            for item in resp.json()[1]:
                print('Result: {}'.format(item))

    @classmethod
    async def get_substitutions_async(cls, on_success=None, on_error=None):
        resp = await cls.get_async('/category/scuba')
        if resp.status_code != 200:
            raise ApiError('GET /substitutions/ {}'.format(resp.status_code))

        if resp.status_code == 200:
            for item in resp.json()[1]:
                print('Result: {}'.format(item))

    @classmethod
    async def get_stop_words_async(cls, on_success=None, on_error=None):
        resp = await cls.get_async('/category/scuba')
        if resp.status_code != 200:
            raise ApiError('GET /stop_words/ {}'.format(resp.status_code))

        if resp.status_code == 200:
            for item in resp.json()[1]:
                print('Result: {}'.format(item))

    @classmethod
    async def get_designated_start_words_async(cls, on_success=None, on_error=None):
        resp = await cls.get_async('/category/scuba')
        if resp.status_code != 200:
            raise ApiError('GET /start_words/ {}'.format(resp.status_code))

        if resp.status_code == 200:
            for item in resp.json()[1]:
                print('Result: {}'.format(item))

    @classmethod
    async def get_designated_end_words_async(cls, on_success=None, on_error=None):
        resp = await cls.get_async('/category/scuba')
        if resp.status_code != 200:
            raise ApiError('GET /end_words/ {}'.format(resp.status_code))

        if resp.status_code == 200:
            for item in resp.json()[1]:
                print('Result: {}'.format(item))

    @classmethod
    async def get_designated_any_words_async(cls, on_success=None, on_error=None):
        resp = await cls.get_async('/category/scuba')
        if resp.status_code != 200:
            raise ApiError('GET /any_words/ {}'.format(resp.status_code))

        if resp.status_code == 200:
            for item in resp.json()[1]:
                print('Result: {}'.format(item))
            
    '''
    sync api
    '''

    @classmethod
    async def get_synonyms(cls, on_success=None, on_error=None):
        resp = cls.get('/category/scuba')
        if resp.status_code != 200:
            raise ApiError('GET /synonyms/ {}'.format(resp.status_code))

        if resp.status_code == 200:
            for item in resp.json()[1]:
                print('Result: {}'.format(item))

    @classmethod
    def get_substitutions(cls, on_success=None, on_error=None):
        resp = cls.get('/category/scuba')
        if resp.status_code != 200:
            raise ApiError('GET /substitutions/ {}'.format(resp.status_code))

        if resp.status_code == 200:
            for item in resp.json()[1]:
                print('Result: {}'.format(item))

    @classmethod
    def get_stop_words(cls, on_success=None, on_error=None):
        resp = cls.get('/category/scuba')
        if resp.status_code != 200:
            raise ApiError('GET /stop_words/ {}'.format(resp.status_code))

        if resp.status_code == 200:
            for item in resp.json()[1]:
                print('Result: {}'.format(item))

    @classmethod
    def get_designated_start_words(cls, on_success=None, on_error=None):
        resp = cls.get('/category/scuba')
        if resp.status_code != 200:
            raise ApiError('GET /start_words/ {}'.format(resp.status_code))

        if resp.status_code == 200:
            for item in resp.json()[1]:
                print('Result: {}'.format(item))

    @classmethod
    def get_designated_end_words(cls, on_success=None, on_error=None):
        resp = cls.get('/category/scuba')
        if resp.status_code != 200:
            raise ApiError('GET /end_words/ {}'.format(resp.status_code))

        if resp.status_code == 200:
            for item in resp.json()[1]:
                print('Result: {}'.format(item))

    @classmethod
    def get_designated_any_words(cls, on_success=None, on_error=None):
        resp = cls.get('/category/scuba')
        if resp.status_code != 200:
            raise ApiError('GET /any_words/ {}'.format(resp.status_code))

        if resp.status_code == 200:
            for item in resp.json()[1]:
                print('Result: {}'.format(item))