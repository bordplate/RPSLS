import curses


class Window(object):
    width = 800
    height = 600

    screen = None
    window = None

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        self.setup()

    def setup(self):
        """
        Sets up the terminal with a window. Waiting to be drawn on.
        :return: None
        """
        self.screen = curses.initscr()

        curses.noecho()  # Don't echo user input
        curses.cbreak()  # React to key-presses instantly
        self.screen.keypad(True)  # Makes it easier to get access to keys like 'KEY_LEFT', etc.

        # Create the window
        self.window = curses.newwin(self.height, self.width, 0, 0)

    def terminal_size_ok(self) -> bool:
        max_y, max_x = self.window.getmaxyx()

        if max_y < self.height or max_x < self.width:
            self.screen.clear()
            return False

        return True

    def clear_screen(self):
        """
        Clears the screen, so it's ready for new draws.
        :return: None
        """
        self.screen.clear()

        # Create border at top and bottom
        for x in range(0, self.width):
            self.safe_addstr(0, x, "█")
            self.safe_addstr(self.height-1, x, "█")

        # Create border left and right
        for y in range(0, self.height):
            self.safe_addstr(y, 0, "█")
            self.safe_addstr(y, self.width-1, "█")

    def safe_addstr(self, y, x, string, mode=0):
        if y < self.height and x < self.width:
            self.screen.addstr(y, x, string, mode)

    def draw_text(self, text: str, x: int, y: int, mode=0):
        """
        Draws text on the screen at coordinates.
        Note that if we don't split them by newline, the newline will render at the far left of the screen.
        :param text: The text you want rendered on sceen.
        :param x: x position
        :param y: y position
        :param mode: Text mode
        :return: None
        """
        for i, string in enumerate(text.split("\n")):
            self.safe_addstr(y+i, x, string, mode)  # Curses has reversed the standard order of x,y for some reason.

    def exit(self):
        """
        Reverses the changes made to terminal in setup() and exits the rendering context.
        :return: None
        """
        curses.nocbreak()
        self.screen.keypad(False)
        curses.echo()
        curses.endwin()
