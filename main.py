import requests
from date_validator import get_date
from tools import *
import curses
import signal


def main():
    """
    The main entry point for the program. Initializes the curses interface and starts the CLI loop.
    Catches exceptions and exits program with an appropriate error message
    """
    try:
        curses.wrapper(cli_loop)
    except curses.error:
        sys.exit(f"\nPlease Exapnd the terminal window and try again\n")
    except Exception as e:
        sys.exit(f"Exception : {e}")


def cli_loop(stdscr_instance):
    """q
    The main loop for the curses interface. Handles user input and displays the table of spaceflight events.

    Parameters:
        stdscr_instance (curses.window): The standard screen window object provided by curses.wrapper.
    """

    global stdscr
    stdscr = stdscr_instance

    beginning_msg = "\n \n \n\t\t\t\t\t\tYOU'VE REACHED THE BEGINNING\n\n\t\t\t\t\t      Enter 'n' to go to the first page \n\t\t\t\t\tStill can't find the event you're looking for? \n\t\t\t\t\tTry running the  program with different dates.".split(
        "\n"
    )
    end_msg = "\n \n \n\t\t\t\t\t\tYOU'VE REACHED THE END\n\n\t\t\t\t\t Enter 'p' to go to the previous page \n\t\t\t\t    Still can't find the event you're looking for? \n\t\t\t\t    Try running the  program with different dates.".split(
        "\n"
    )

    previous_page = None
    next_page = None

    args = get_args()
    check_args(args)

    count, next, previous, table_lines = get_table_data(args)

    curses.curs_set(0)  # Hide the cursor
    stdscr.clear()
    signal.signal(signal.SIGWINCH, resize_handler)
    max_y, max_x = stdscr.getmaxyx()
    win = curses.newwin(max_y - 7, max_x - 1, 5, 0)

    start_line = 0
    start_col = 0
    run_loop = True

    while run_loop:
        try:
            stdscr.addstr(0, 45, "SPACEFLIGHT EVENTS LIBRARY", curses.A_UNDERLINE)
            stdscr.addstr(
                1,
                0,
                " Click any arrow key to display the data\n Use arrow keys to navigate\n To exit the program press 'q'",
            )
            stdscr.addstr(
                max_y - 1,
                0,
                "For more info about the events visit: https://thespacedevs.com/llapi",
            )
            stdscr.addstr(4, 0, " Press 'n' or 'p' to go 'next page' or previous page'")
            max_y, max_x = stdscr.getmaxyx()
            win.resize(max_y - 7, max_x - 1)
            win.clear()
            end_line = min(start_line + max_y - 7, len(table_lines))

            for idx, line in enumerate(table_lines[start_line:end_line]):
                try:
                    win.addstr(idx, 0, line[start_col : start_col + max_x - 1])
                except curses.error:
                    pass  # Ignore addstr errors
            stdscr.refresh()
            win.refresh()

        except curses.error:
            stdscr.addstr(6, 0, "\n\t\t\t\t\tPLAESE EXPAND THE WINDOW")
            stdscr.refresh()
            key = stdscr.getch()
            if key == ord("q"):
                run_loop = False
            continue

        else:
            key = stdscr.getch()

            if key == curses.KEY_DOWN and end_line < len(table_lines):
                start_line += 1
            elif key == curses.KEY_UP and start_line > 0:
                start_line -= 1
            elif key == curses.KEY_RIGHT:
                start_col += 1
            elif key == curses.KEY_LEFT and start_col > 0:
                start_col -= 1
            elif (key == ord("n") or key == ord('N')):
                if table_lines == end_msg:
                    continue
                elif count and next_page:
                    table_lines = next_page
                    next_page = None
                elif next:
                    win.clear()
                    win.addstr("\n\n\n\t\t\t\t\t\tPLEASE WAIT...")
                    win.refresh()
                    stdscr.refresh()
                    count, next, previous, table_lines = get_table_data(args, url=next)
                else:
                    if count:
                        previous_page = table_lines.copy()
                    table_lines = end_msg

            elif (key == ord("p") or key == ord('P')):
                if table_lines == beginning_msg:
                    continue
                elif count and previous_page:
                    table_lines = previous_page
                    previous_page = None
                elif previous:
                    win.clear()
                    win.addstr("\n\n\n\t\t\t\t\t\tPLEASE WAIT...")
                    win.refresh()
                    stdscr.refresh()
                    count, next, previous, table_lines = get_table_data(
                        args, url=previous
                    )
                else:
                    if count:
                        next_page = table_lines.copy()
                    table_lines = beginning_msg
            elif (key == ord("q") or key == ord('Q')):
                run_loop = False


def get_events_url(start_date, end_date, is_today=False):
    """
    Constructs the URL for querying spaceflight events based on the provided date range or for today's date.

    Parameters:
        start_date (str): The start date in the format 'DD-MM-YYYY'.
        end_date (str): The end date in the format 'DD-MM-YYYY'.
        is_today (bool): If True, fetches events for today only.

    Returns:
        str: The constructed query URL.
    """
    event_base_url = "https://lldev.thespacedevs.com/2.2.0/event/"
    filters = []
    if not start_date:
        start_date = datetime.now() - timedelta(days=15)
    else:
        start_date = get_date(start_date)
    if not end_date:
        end_date = datetime.now() + timedelta(days=15)
    else:
        end_date = get_date(end_date)
    if is_today:
        d, m, y = list(map(str, get_todays_date()))
        day = "day=" + d
        month = "month=" + m
        year = "year=" + y
        date = "&".join((day, month, year))
        filters.append(date)
    else:
        date_filters = add_date_filters(start_date, end_date)
        filters.append(date_filters)
    query_url = event_base_url + "?" + "&".join(filters)
    return query_url


def get_table_data(args, url=None):
    """
    Fetches the event data from the API and constructs the table data for display.

    Parameters:
        args (object): The arguments object containing start_date, end_date, and today attributes.
        url (str)(optional): The URL to fetch data from. If None, constructs the URL using start_date and end_date from args.

    Returns:
        tuple: A tuple containing the count of events, next URL, previous URL, and the table lines.

    Raises:
        ConnectionError: If the status code of the response is not 200.
    """
    if not url:
        query_url = get_events_url(args.start_date, args.end_date, is_today=args.today)
    else:
        query_url = url
    results = requests.get(query_url)

    status = results.status_code
    if status != 200:
        raise ConnectionError("Error : couldn't get the data\n Status code : {status}")
    result = results.json()
    return create_df(result)


def resize_handler(signum, frame):
    """
    Signal handler for terminal resize events. Reinitializes the curses window to handle the new terminal size.

    Parameters:
        signum (int): The signal number.
        frame (frame object): The current stack frame.
    """
    curses.endwin()
    curses.initscr()
    curses.resizeterm(*stdscr.getmaxyx())
    stdscr.clear()


if __name__ == "__main__":
    main()
