import httpx
import asyncio


class ApiError(Exception):
    def __init__(self, status):
        self.status = status

    def __str__(self):
        return "API Error: status={}".format(self.status)


class AbstractApiClient:
    _async_client = httpx.AsyncClient()
    _client = httpx.Client()
    _base_uri = ''

    @classmethod
    def handle_error(cls, resp, on_error=lambda x: None):
        on_error(resp)
        raise ApiError('GET / {}'.format(resp.status_code))

    @classmethod
    def handle_success(cls, resp, on_success=lambda x: None):
        for item in resp.json()[1]:
            print('Result: {}'.format(item))

        on_success(resp)

    '''
    async api
    '''

    @classmethod
    async def options_async(cls, path):
        try:
            async with cls._async_client as client:
                return client.get(cls._base_uri + path)
        except Exception as error:
            print(error)

    @classmethod
    async def get_async(cls, path):
        try:
            async with cls._async_client as client:
                return client.get(cls._base_uri + path)
        except Exception as error:
            print(error)

    @classmethod
    async def post_async(cls, path):
        try:
            async with cls._async_client as client:
                return client.post(cls._base_uri + path)
        except Exception as error:
            print(error)

    @classmethod
    async def put_async(cls, path):
        try:
            async with cls._async_client as client:
                return client.put(cls._base_uri + path)
        except Exception as error:
            print(error)

    @classmethod
    async def patch_async(cls, path):
        try:
            async with cls._async_client as client:
                return client.patch(cls._base_uri + path)
        except Exception as error:
            print(error)

    @classmethod
    async def delete_async(cls, path):
        try:
            async with cls._async_client as client:
                return client.delete(cls._base_uri + path)
        except Exception as error:
            print(error)

    '''
    sync api
    '''

    @classmethod
    def options(cls, path):
        try:
            with cls._client as client:
                return client.options(cls._base_uri + path)
        except Exception as error:
            print(error)
            raise error

    @classmethod
    def get(cls, path):
        try:
            with cls._client as client:
                return client.get(cls._base_uri + path)
        except Exception as error:
            print(error)
            raise error

    @classmethod
    def post(cls, path):
        try:
            with cls._client as client:
                return client.post(cls._base_uri + path)
        except Exception as error:
            print(error)
            raise error

    @classmethod
    def put(cls, path):
        try:
            with cls._client as client:
                return client.put(cls._base_uri + path)
        except Exception as error:
            print(error)
            raise error

    @classmethod
    def patch(cls, path):
        try:
            with cls._client as client:
                return client.patch(cls._base_uri + path)
        except Exception as error:
            print(error)
            raise error

    @classmethod
    def delete(cls, path):
        try:
            with cls._client as client:
                return client.delete(cls._base_uri + path)
        except Exception as error:
            print(error)
            raise error
