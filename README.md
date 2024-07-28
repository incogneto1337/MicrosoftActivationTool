# Microsoft Activation Tool

This Python CLI tool uses the `curses` library to provide an interactive menu for running a predefined PowerShell command. The command fetches and executes a script from the specified URL using `irm` (Invoke-RestMethod) and `iex` (Invoke-Expression).

## Features

- Interactive menu interface using `curses`.
- Execute a predefined PowerShell command.
- Display command output within the CLI interface.

## Prerequisites

- Python 3.x
- PowerShell
- `curses` library (included in the Python Standard Library)

## Installation

1. Ensure you have Python 3 installed on your system.
2. Clone this repository or copy the script into a Python file.

## Usage

Run the script using Python:

```sh
python mat.py
```

### Menu Options

1. **Run PowerShell Command**: Executes the predefined PowerShell command and displays the output.
2. **Exit**: Exits the program.

## Script Breakdown

### `run_powershell_command(command)`

Executes a given PowerShell command and captures its output.

```python
def run_powershell_command(command):
    try:
        result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"An error occurred: {e}\nError output:\n{e.stderr}"
```

### `display_menu(stdscr)`

Displays the interactive menu and handles user input for navigation and selection.

```python
def display_menu(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    stdscr.refresh()

    menu = ["Run PowerShell Command", "Exit"]
    current_row = 0

    # Set up color pair for highlighting selected menu item
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        for idx, row in enumerate(menu):
            x = width // 2 - len(row) // 2
            y = height // 2 - len(menu) // 2 + idx
            if idx == current_row:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, row)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, row)

        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if current_row == 0:
                stdscr.clear()
                stdscr.addstr(0, 0, "Running PowerShell command...")
                stdscr.refresh()
                output = run_powershell_command("irm https://get.activated.win | iex")
                stdscr.clear()
                stdscr.addstr(0, 0, output)
                stdscr.refresh()
                stdscr.getch()
            elif current_row == 1:
                break
```

### `main(stdscr)`

Main function wrapped with `curses.wrapper` to initialize the curses application.

```python
def main(stdscr):
    display_menu(stdscr)

if __name__ == "__main__":
    curses.wrapper(main)
```

## Notes

- This script runs a predefined PowerShell command that downloads and executes a script from the internet. Ensure you trust the source of the script to avoid security risks.
- The tool uses the `curses` library to create a text-based user interface. This library may not be available on all platforms, especially Windows. Consider using a compatible terminal emulator or a different environment if issues arise.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

---

