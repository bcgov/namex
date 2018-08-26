from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import DateTime


class utcnow(expression.FunctionElement):
    type = DateTime()


@compiles(utcnow, 'postgresql')
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


class utcnow_minus(expression.FunctionElement):
    type = DateTime()


@compiles(utcnow_minus, 'postgresql')
def pg_utcnow_minus(element, compiler, min, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP- (20 ||' minutes')::interval)"
