import curses
import subprocess

def run_powershell_command(command):
    try:
        result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"An error occurred: {e}\nError output:\n{e.stderr}"

def display_menu(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    stdscr.refresh()

    menu = ["Run PowerShell Command", "Exit"]
    current_row = 0

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        for idx, row in enumerate(menu):
            x = width//2 - len(row)//2
            y = height//2 - len(menu)//2 + idx
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

def main():
    curses.wrapper(display_menu)

if __name__ == "__main__":
    curses.wrapper(main)
