import re
import datetime

pattern = r"^(0[1-9]|[1-9]|[12][0-9]|3[01])-(0[1-9]|[1-9]|1[0-2])-(\d{4})$"


def is_leap_year(year):
    """
    Determines whether the specified year is a leap year.

    Parameters:
        year (int): The year to check.

    Returns:
        bool: True if the year is a leap year, False otherwise.
    """
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def validate_date(date_str):
    """
    Validates the given date string to ensure it is a valid date.

    Parameters:
        date_str (str): The date string in the format 'DD-MM-YYYY'.

    Returns:
        bool: True if the date string represents a valid date, False otherwise.
    """
    if not re.match(pattern, date_str):
        return False  # Not a valid date format

    day, month, year = map(int, date_str.split("-"))
    if month in [4, 6, 9, 11] and day > 30:
        return False  # April, June, September, November have 30 days
    elif month == 2:
        if day > 29:
            return False  # February has 29 days in a leap year
        if day == 29 and not is_leap_year(year):
            return False  # February 29 is only valid in a leap year

    return True


def get_date(date):
    """
    Converts a date string into a datetime.date object.

    Parameters:
        date (str): The date string in the format 'DD-MM-YYYY'.

    Returns:
        datetime.date: A date object representing the given date.
    """
    day, month, year = re.match(pattern, date).groups()
    return datetime.date(int(year), int(month), int(day))
