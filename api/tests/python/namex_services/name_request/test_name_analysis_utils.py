import pytest

from namex.services.name_request.auto_analyse.name_analysis_utils import remove_french


@pytest.mark.parametrize("name, expected",
                         [
                             ("CENTRAL CARE CORPORATION/CORPORATION CENTRALE DE SOINS", "CENTRAL CARE CORPORATION"),
                             ("20/20 CAFE & BAKERY", "20/20 CAFE & BAKERY"),
                             ("ABC ENGINEERING/CENTRAL CARE CORP.", "ABC ENGINEERING"),
                             ("RE/MAX WALNUT DEVELOPERS", "RE/MAX WALNUT DEVELOPERS")
                         ]
                         )
def test_remove_french(name, expected):
    assert remove_french(name) == expected
