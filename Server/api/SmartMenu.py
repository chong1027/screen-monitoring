# api.py
import platform
import time
import sys
class SmartMenu:
    def __init__(self, options,selected,top=0):
        self.options = options
        self.selected = selected if selected != sys.maxsize else 0
        self.os_name = platform.system()
        self.top = top

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
            now=0
            for i, option in enumerate(self.options):
                if self.top == 0:
                    if i == self.selected:
                        print(f"> {option} <")
                    else:
                        print(f"  {option}")
                else:
                    if i < self.top:
                        print(f"  {option}")
                    elif i == self.selected + self.top:
                        print(f"> {option} <")
                    else:
                        print(f"  {option}")
        start_time = time.time()
        while True and time.time() - start_time < 1:
            print_menu()
            key = msvcrt.getch()

            if key == b'\xe0':  # Special key prefix
                next_key = msvcrt.getch()
                if next_key == b'H':  # Up arrow
                    self.selected = (self.selected - 1) % (len(self.options) - self.top)
                elif next_key == b'P':  # Down arrow
                    self.selected = (self.selected + 1) % (len(self.options) - self.top)

            elif key == b'\r':  # Enter
                return self.selected

            elif key == b'\x1b':  # ESC
                return None

    def _unix_menu(self):
        import curses

        def menu(stdscr):
            curses.curs_set(0)
            start_time = time.time()
            while True and time.time() - start_time < 5:
                stdscr.clear()
                h, w = stdscr.getmaxyx()

                for i, option in enumerate(self.options):
                    x = w//2 - len(option)//2
                    y = h//2 - len(self.options)//2 + i
                    if self.top == 0:
                        if i == self.selected:
                            stdscr.attron(curses.A_REVERSE)
                            stdscr.addstr(y, x, option)
                            stdscr.attroff(curses.A_REVERSE)
                        else:
                            stdscr.addstr(y, x, option)
                    else:
                        if i < self.top:
                            stdscr.addstr(y, x, option)
                        elif i == self.selected + self.top:
                            stdscr.attron(curses.A_REVERSE)
                            stdscr.addstr(y, x, option)
                            stdscr.attroff(curses.A_REVERSE)
                        else:
                            stdscr.addstr(y, x, option)
                key = stdscr.getch()

                if key == curses.KEY_UP:
                    self.selected = abs(self.selected - 1) % (len(self.options)-self.top)
                elif key == curses.KEY_DOWN:
                    self.selected = (self.selected + 1) % (len(self.options)-self.top)
                elif key in [curses.KEY_ENTER, 10, 13]:
                    return self.selected
                elif key == 27:  # ESC
                    return None

        return curses.wrapper(menu)