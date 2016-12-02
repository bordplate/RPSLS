import curses


class Window(object):
    """
    Window is responsible for drawing on the screen.
    """

    width = 0
    height = 0

    screen = None  # A curses screen
    window = None  # A curses window

    def __init__(self, width: int, height: int):
        """
        Sets desired size for our window.
        :param width: The width we want
        :param height: The height we want
        """
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

        self.window.resize(self.height, self.width)

    def terminal_size_ok(self) -> bool:
        """
        Checks whether or not the user's terminal size is big enough for our program.
        :return: True if terminal is big enough, False if it is not.
        """
        max_y, max_x = self.screen.getmaxyx()  # Gets the size of the user's terminal.

        # If the terminal is not big enough, clear right away to avoid crashes.
        if max_y < self.height or max_x < self.width:
            self.screen.clear()
            return False

        return True

    def clear_screen(self):
        """
        Clears the screen, so it's ready for new draws.
        Also adds a border around the screen.
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
        max_y, max_x = self.screen.getmaxyx()
        if max_y-1 > y >= 0 and max_x-1 > x >= 0:
            self.screen.addstr(y, x, string, mode)
        else:
            self.window.resize(max_y, max_x)

    def draw_text(self, text: str, x: int, y: int):
        """
        Draws text on the screen at coordinates.
        Note that if we don't split them by newline, the newline will render at the far left of the screen.
            Would be different if all sprites had `\n'-line endings, but Windows adds `\r\n' as line endings.
        :param text: The text you want rendered on screen.
        :param x: x position
        :param y: y position
        :return: None
        """
        for i, string in enumerate(text.split("\n")):
            self.safe_addstr(y+i, x, string)  # Curses has reversed the standard order of x,y for some reason.

    def exit(self):
        """
        Reverses the changes made to terminal in setup() and exits the rendering context.
        :return: None
        """
        curses.nocbreak()
        self.screen.keypad(False)
        curses.echo()
        curses.endwin()
