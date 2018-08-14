from namex.services.nro import NROServicesError
import pytest


def test_nro_exception():
    """checking that the error can be raised
       and that the parts get set correctly
    """
    with pytest.raises(NROServicesError) as e_info:
        raise NROServicesError ({"code":"test_error",
                                 "description": "used to test the error functionality"}
                                ,500)

    assert e_info.value.status_code == 500
    assert e_info.value.error == {"code":"test_error",
                                 "description": "used to test the error functionality"}
