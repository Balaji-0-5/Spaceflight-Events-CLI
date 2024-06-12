from datetime import datetime, timedelta
import pandas as pd
import pytest
from tools import *
from unittest.mock import patch, Mock

mock_data = {
    "count": 1,
    "next": "http://example.com/next",
    "previous": "http://example.com/previous",
    "results": [
        {
            "id": 1,
            "name": "Event 1",
            "date": "2023-01-01T00:00:00Z",
            "description": "Description of Event 1",
            "url": "http://example.com",
            "duration": "1 hour",
            "webcast_live": True,
            "location": "Location 1",
            "news_url": "http://example.com/news",
            "video_url": "http://example.com/video",
            "feature_image": "http://example.com/image",
            "slug": "event-1",
            "last_updated": "2023-01-01T00:00:00Z",
        }
    ],
}


def test_create_df():
    count, next_url, prev_url, tabulated_data = create_df(mock_data)
    assert count == 1
    assert next_url == "http://example.com/next"
    assert prev_url == "http://example.com/previous"
    assert isinstance(tabulated_data, list)
    assert len(tabulated_data) > 0


def test_add_date_filters():
    start_date = datetime.now().date()
    end_date = start_date + timedelta(days=10)
    date_filters = add_date_filters(start_date, end_date)
    assert isinstance(date_filters, str)
    assert "date__gte=" in date_filters
    assert "date__lte=" in date_filters


def test_get_todays_date():
    today = datetime.now().date()
    day, month, year = get_todays_date()
    assert day == today.day
    assert month == today.month
    assert year == today.year


def test_tabulate_data():
    df = pd.DataFrame(mock_data["results"])
    tabulated_data = tabulate_data(df)
    assert isinstance(tabulated_data, list)
    assert len(tabulated_data) > 0


@patch("tools.sys.exit")
@patch("tools.validate_date")
def test_check_args(mock_validate_date, mock_sys_exit):
    # Test case 1: Today option is used with start_date or end_date
    args = Mock()
    args.today = True
    args.start_date = "01-01-2022"
    args.end_date = None
    check_args(args)
    mock_sys_exit.assert_called_with(
        "Can't use both today and (start or end) at the same time"
    )

    # Test case 2: Invalid start_date format
    args.today = False
    args.start_date = "2022-01-01"
    args.end_date = None
    mock_validate_date.return_value = False
    check_args(args)
    mock_sys_exit.assert_called_with(
        "Please enter a valid start date in the format DD-MM-YYYY"
    )

    # Test case 3: Invalid end_date format
    args.start_date = None
    args.end_date = "2022-01-01"
    mock_validate_date.return_value = False
    check_args(args)
    mock_sys_exit.assert_called_with(
        "Please enter a valid end date in the format DD-MM-YYYY"
    )


@patch("tools.argparse.ArgumentParser.parse_args")
def test_get_args(mock_parse_args):
    # Test case 1: Only -t/--today option is used
    mock_parse_args.return_value = Mock(today=True, start_date=None, end_date=None)
    args = get_args()
    assert args.today == True
    assert args.start_date == None
    assert args.end_date == None

    # Test case 2: -s/--start and -e/--end options are used
    mock_parse_args.return_value = Mock(
        today=False, start_date="01-01-2022", end_date="31-01-2022"
    )
    args = get_args()
    assert args.today == False
    assert args.start_date == "01-01-2022"
    assert args.end_date == "31-01-2022"
