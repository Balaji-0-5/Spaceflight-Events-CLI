from datetime import datetime, timedelta, UTC
from date_validator import validate_date
from tabulate import tabulate
import pandas as pd
import sys
import textwrap
import argparse


def create_df(data):
    """
    Converts the event data into a pandas DataFrame, wraps text in the description column,
    and formats the DataFrame as a table string.

    Parameters:
        data (dict): The event data in JSON format.

    Returns:
        tuple: A tuple containing the count of events, the next URL, the previous URL, and
               the tabulated data as a list of strings.
    """
    count = data["count"]
    next = data["next"]
    previous = data["previous"]
    if count == 0:
        return (
            count,
            next,
            previous,
            "\n \n \n\t\t\t\t\t\t NO EVENTS\n \n \n".split("\n"),
        )
    df = pd.DataFrame(data["results"]).set_index("id")

    def wrap_text(text, width=40):
        return "\n".join(textwrap.wrap(text, width=width))

    df["description"] = df["description"].apply(
        lambda x: wrap_text(x) if isinstance(x, str) else x
    )

    static_fields = [
        "name",
        "date",
        "description",
        "url",
        "duration",
        "webcast_live",
        "location",
        "news_url",
        "video_url",
        "feature_image",
        "slug",
        "last_updated",
    ]
    df = df[static_fields]
    return count, next, previous, tabulate_data(df)


def add_date_filters(start, end):
    """
    Creates date filters for API query based on the given start and end dates.

    Parameters:
        start (datetime.date): The start date for the filter.
        end (datetime.date): The end date for the filter.

    Returns:
        str: A string representing the date filters in query format.
    """
    from_date = f"date__gte={start}"
    to_date = f"date__lte={end}"
    return "&".join((from_date, to_date))


def get_todays_date():
    """
    Retrieves today's date.

    Returns:
        tuple: A tuple containing the day, month, and year of today's date.
    """
    now = datetime.now(UTC)
    day = now.day
    month = now.month
    year = now.year
    return day, month, year


def tabulate_data(df):
    """
    Converts the given DataFrame into a tabulated string format.

    Parameters:
        df (pandas.DataFrame): The DataFrame to be tabulated.

    Returns:
        list: A list of strings representing the tabulated data.
    """
    return tabulate(df, headers="keys", tablefmt="grid").split("\n")


def get_args():
    """
    Parses command-line arguments.

    Returns:
        argparse.Namespace: The parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Displays the spaceflight events in a given time interrval  in tabular form.\nDefaulty displays events from 15 days before to 15 days after today"
    )

    parser.add_argument(
        "-s",
        "--start",
        dest="start_date",
        help="Enter the date from which you want the data to be displayed.\nPlease use the DD-MM-YYYY format\n(default: 15 days before today)",
    )
    parser.add_argument(
        "-e",
        "--end",
        dest="end_date",
        help="Enter the date until which you want the data to be displayed.\nPlease use the DD-MM-YYYY format\n(default: 15 days after today)",
    )
    parser.add_argument(
        "-t", "--today", action="store_true", help="Displays the events of today"
    )

    return parser.parse_args()


def check_args(args):
    """
    Validates the command-line arguments.

    Parameters:
        args (argparse.Namespace): The parsed command-line arguments.

    Exits:
        If the arguments are invalid or conflicting.
    """
    start_date = args.start_date
    end_date = args.end_date
    if args.today:
        if start_date or end_date:
            sys.exit("Can't use both today and (start or end) at the same time")
    else:
        if start_date:
            if not validate_date(start_date):
                sys.exit("Please enter a valid start date in the format DD-MM-YYYY")
        if end_date:
            if not validate_date(end_date):
                sys.exit("Please enter a valid end date in the format DD-MM-YYYY")
