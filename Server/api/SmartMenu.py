# api.py
import platform

class SmartMenu:
    def __init__(self, options):
        self.options = options
        self.selected = 0
        self.os_name = platform.system()
    
    def show(self):
        if self.os_name == 'Windows':
            return self._windows_menu()
        else:
            return self._unix_menu()

    def _windows_menu(self):
        import msvcrt
        import os

        def clear_screen():
            os.system('cls')

        def print_menu():
            clear_screen()
            for i, option in enumerate(self.options):
                if i == self.selected:
                    print(f"> {option} <")
                else:
                    print(f"  {option}")

        while True:
            print_menu()
            key = msvcrt.getch()

            if key == b'\xe0':  # Special key prefix
                next_key = msvcrt.getch()
                if next_key == b'H':  # Up arrow
                    self.selected = (self.selected - 1) % len(self.options)
                elif next_key == b'P':  # Down arrow
                    self.selected = (self.selected + 1) % len(self.options)

            elif key == b'\r':  # Enter
                return self.selected

            elif key == b'\x1b':  # ESC
                return None

    def _unix_menu(self):
        import curses

        def menu(stdscr):
            curses.curs_set(0)

            while True:
                stdscr.clear()
                h, w = stdscr.getmaxyx()

                for i, option in enumerate(self.options):
                    x = w//2 - len(option)//2
                    y = h//2 - len(self.options)//2 + i
                    if i == self.selected:
                        stdscr.attron(curses.A_REVERSE)
                        stdscr.addstr(y, x, option)
                        stdscr.attroff(curses.A_REVERSE)
                    else:
                        stdscr.addstr(y, x, option)

                key = stdscr.getch()

                if key == curses.KEY_UP:
                    self.selected = (self.selected - 1) % len(self.options)
                elif key == curses.KEY_DOWN:
                    self.selected = (self.selected + 1) % len(self.options)
                elif key in [curses.KEY_ENTER, 10, 13]:
                    return self.selected
                elif key == 27:  # ESC
                    return None

        return curses.wrapper(menu)