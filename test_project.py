from project import *
from datetime import datetime, timedelta, UTC
import pytest
import warnings
from unittest import mock


@mock.patch("project.get_args")
@mock.patch("project.check_args")
@mock.patch("project.get_table_data")
@mock.patch("curses.curs_set")
@mock.patch("curses.newwin")
def test_cli_loop(
    mock_newwin, mock_curs_set, mock_get_table_data, mock_check_args, mock_get_args
):
    mock_get_args.return_value = mock.Mock(
        start_date="01-01-2023", end_date="31-01-2023", today=False
    )
    mock_check_args.return_value = None
    mock_get_table_data.return_value = (1, None, None, ["name", "Event 1"])

    mock_stdscr_instance = mock.Mock()
    mock_stdscr_instance.getmaxyx.return_value = (24, 80)
    mock_stdscr_instance.getch.side_effect = [ord("q")]
    mock_stdscr_instance.clear.return_value = mock.Mock()

    mock_window_instance = mock.Mock()
    mock_newwin.return_value = mock_window_instance

    # Simulate a global stdscr
    global stdscr
    stdscr = mock_stdscr_instance

    cli_loop(mock_stdscr_instance)

    mock_check_args.assert_called_once_with(mock_get_args.return_value)
    mock_curs_set.assert_called_once_with(0)
    mock_stdscr_instance.clear.assert_called_once()
    mock_stdscr_instance.addstr.assert_any_call(
        0, 45, "SPACEFLIGHT EVENTS LIBRARY", curses.A_UNDERLINE
    )
    mock_stdscr_instance.addstr.assert_any_call(
        1,
        0,
        " Click any arrow key to display the data\n Use arrow keys to navigate\n To exit the program press 'q'",
    )
    mock_stdscr_instance.addstr.assert_any_call(
        23, 0, "For more info about the events visit: https://thespacedevs.com/llapi"
    )
    mock_stdscr_instance.addstr.assert_any_call(
        4, 0, " Press 'n' or 'p' to go 'next page' or previous page'"
    )

    mock_window_instance.resize.assert_called_once_with(17, 79)
    mock_window_instance.clear.assert_called_once()
    mock_stdscr_instance.refresh.assert_called()
    mock_window_instance.refresh.assert_called()


def test_get_events_url():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
    # Test case 1: Test with specific start and end dates
    start_date = "01-01-2023"
    end_date = "31-01-2023"
    expected_url = "https://lldev.thespacedevs.com/2.2.0/event/?date__gte=2023-01-01&date__lte=2023-01-31"
    assert get_events_url(start_date, end_date) == expected_url

    # Test case 2: Test with today's date
    today = datetime.now(UTC).strftime("%d-%m-%Y")
    expected_today_url = f"https://lldev.thespacedevs.com/2.2.0/event/?day={today.split('-')[0]}&month={today.split('-')[1][1]}&year={today.split('-')[2]}"
    assert get_events_url(None, None, is_today=True) == expected_today_url


@mock.patch("project.requests.get")
def test_get_table_data(mock_requests_get):
    mock_args = mock.Mock(start_date="01-01-2023", end_date="31-01-2023", today=False)
    mock_requests_get.return_value = mock.Mock(
        **{
            "status_code": 200,
            "json.return_value": {
                "count": 1,
                "next": None,
                "previous": None,
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
            },
        }
    )
    requests.get = mock_requests_get
    count, next_url, previous_url, table_lines = get_table_data(mock_args)

    assert count == 1
    assert next_url is None
    assert previous_url is None
    assert "name" in table_lines[1]

    mock_requests_get = mock.Mock(status_code=404)
    requests.get = mock_requests_get
    with pytest.raises(
        ConnectionError, match="Error : couldn't get the data\n Status code : {status}"
    ):
        get_table_data(mock_args)


@mock.patch("curses.endwin")
@mock.patch("curses.initscr")
@mock.patch("curses.resizeterm")
@mock.patch("builtins.globals")
def test_resize_handler(mock_globals, mock_resizeterm, mock_initscr, mock_endwin):
    stdscr = mock.Mock()
    stdscr.getmaxyx.return_value = (24, 80)
    mock_globals.return_value = {"stdscr": stdscr}

    resize_handler(signal.SIGWINCH, mock.Mock())

    mock_endwin.assert_called_once()
    mock_initscr.assert_called_once()
    mock_resizeterm.assert_called_once_with(24, 80)
