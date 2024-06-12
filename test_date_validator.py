import pytest
from date_validator import *


@pytest.fixture(params=[(2000, True), (1900, False), (2024, True), (2021, False)])
def leap_year_data(request):
    return request.param


def test_is_leap_year(leap_year_data):
    year, expected_result = leap_year_data
    assert is_leap_year(year) == expected_result


@pytest.fixture(
    params=[
        ("29-02-2000", True),
        ("29-02-2001", False),
        ("31-04-2022", False),
        ("31-06-2022", False),
        ("31-09-2022", False),
        ("31-11-2022", False),
        ("30-06-2022", True),
    ]
)
def date_validation_data(request):
    return request.param


def test_validate_date(date_validation_data):
    date_str, expected_result = date_validation_data
    assert validate_date(date_str) == expected_result


@pytest.fixture(
    params=[
        ("29-02-2000", datetime.date(2000, 2, 29)),
        ("30-04-2022", datetime.date(2022, 4, 30)),
    ]
)
def date_conversion_data(request):
    return request.param


def test_get_date(date_conversion_data):
    date_str, expected_date = date_conversion_data
    assert get_date(date_str) == expected_date
