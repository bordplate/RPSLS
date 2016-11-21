from time import sleep


class Engine(object):
    """
    Engine responsible for rendering logic and game ticks.
    """
    SLEEP_INTERVAL = 0.0416667  # Gives about 24FPS

    ticks = 0

    window = None
    running = False

    scene = None

    def __init__(self, window):
        self.window = window

    def start(self):
        self.running = True
        self.run()

    def run(self):
        """
        Does backend running of the game,
            passes logic on to tick()
            and render() when appropriate.
        Does an infinite loop until running
            is set to `False'.
        :return: None
        """
        while self.running:
            self.tick()
            self.render()
            sleep(self.SLEEP_INTERVAL)        # Should sleep so we get around 24FPS

    def tick(self):
        """
        Passes on to the current running scene,
            which is, in turn, responsible for
            making sure it's objects update.
        :return: None
        """

        self.ticks += 1

        if self.scene:
            self.scene.tick()

    def render(self):
        """
        Renders the screen with appropriate data from current scene.
        :return: None
        """
        self.window.drawText("Ticks: " + str(self.ticks))
        if self.scene:
            self.scene.render()

        self.window.refresh()
