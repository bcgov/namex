"""CORS pre-flight decorator

"""
from functools import wraps

def cors_preflight(methods):
    def wrapper(f):

        def options(self,  *args, **kwargs):
            return {'Allow': 'GET'}, 200, \
                   {'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': methods,
                    'Access-Control-Allow-Headers': 'Authorization, Content-Type'}

        setattr(f, 'options', options)
        return f
    return wrapper