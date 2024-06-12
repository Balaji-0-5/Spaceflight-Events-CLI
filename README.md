# Spaceflight Events CLI

#### Video Demo:  <URL https://youtu.be/vm1y4vHlUMk>
## Description:
This project is a command-line tool that fetches and displays upcoming spaceflight events in a tabular format. It interacts with a public API to retrieve event data, allowing users to specify a date range or view events for the current day. The tool provides navigation options to browse through the events easily. The data for this project was sourced from [The Space Devs API](https://thespacedevs.com/llapi).

## Features

- Display spaceflight events in a tabular format.
- Navigate through events using arrow keys.
- Filter events by a specified date range.
- Fetch events for today.
- Automatically adjust display based on terminal size.
## Requirements
- Python 3.6+
- `requests` library
- `pandas` library
- `tabulate` library
- `curses` library (usually available by default in Python installations)

## File Descriptions
- **`project.py`**: Contains the main logic for fetching, processing, and displaying event data using the curses library.
- **`date_validator.py`**: Provides functions to validate dates in the format `DD-MM-YYYY`.
- **`tools.py`**: Includes utility functions used by the project script.

## Usage
- Run `project.py` to start the program.
- Navigate through events using arrow keys.
- Use `n` to go to the next page, `p` to go to the previous page, and `q` to quit.


## Run
 `
  $ python project.py [-h] [-s START_DATE] [-e END_DATE] [-t]
 `
 - Specify date ranges with `-s` (start date) and `-e` (end date), or use `-t` to view events for the current day.
 - Date format `DD-MM-YYYY`
## Design Choices
- **Curses Library**: Utilized for a text-based interface, providing an interactive and visually appealing experience in the terminal.
- **Tabulate for Formatting**: Used to format event data into a table, improving readability and navigation.


## Future Enhancements
- Additional date filtering options, such as specifying ranges of years or months.
- Implementation of caching for reduced API requests and improved performance.
- Enhanced user interface features like color highlighting or more detailed event information.


## License
- This project is licensed under the terms of the MIT License.

