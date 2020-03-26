import pytest

from namex.services.name_request.auto_analyse.name_analysis_utils import remove_french, list_distinctive_descriptive


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


@pytest.mark.parametrize("name_list, dist_list, desc_list, dist_expected, desc_expected",
                         [
                             (['PACIFIC', 'BLUE', 'ENTERPRISE'], ['PACIFIC', 'BLUE', 'ENTERPRISE'], ['PACIFIC', 'ENTERPRISE'],
                              [['PACIFIC', 'BLUE']], [['ENTERPRISE']]),
                             (['PACIFIC', 'BLUE', 'COAST', 'ENTERPRISE'], ['PACIFIC', 'BLUE', 'COAST', 'ENTERPRISE'], ['PACIFIC', 'COAST', 'ENTERPRISE'],
                              [['PACIFIC', 'BLUE'], ['PACIFIC', 'BLUE', 'COAST']], [['COAST', 'ENTERPRISE'], ['ENTERPRISE']])
                         ]
                         )
def test_list_distinctive_descriptive(name_list, dist_list, desc_list, dist_expected, desc_expected):
    assert list_distinctive_descriptive(name_list, dist_list, desc_list) == (dist_expected, desc_expected)
