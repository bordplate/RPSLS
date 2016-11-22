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

    def clear_screen(self):
        """
        Clears the screen, so it's ready for new draws.
        :return: None
        """
        self.screen.clear()

    def draw_text(self, text: str, x: int, y: int):
        """
        Draws text on the screen at coordinates.
        Note that if we don't split them by newline, the newline will render at the far left of the screen.
        :param text: The text you want rendered on sceen.
        :param x: x position
        :param y: y position
        :return: None
        """
        for i, string in enumerate(text.split("\n")):
            self.screen.addstr(y+i, x, string)  # Curses has reversed the standard order of x,y for some reason.

    def refresh(self):
        self.screen.refresh()

    def exit(self):
        """
        Reverses the changes made to terminal in setup() and exits the rendering context.
        :return: None
        """

        curses.nocbreak()
        self.screen.keypad(False)
        curses.echo()
        curses.endwin()
