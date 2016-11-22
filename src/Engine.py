from time import sleep
import sys
import curses


class Engine(object):
    """
    Engine responsible for rendering logic and game ticks.
    """
    SLEEP_INTERVAL = 0.0416667  # Gives about 24FPS

    window = None
    running = False

    ticks = 0

    scene = None

    def __init__(self, window):
        self.window = window

    def start(self):
        """
        Fires up the game engine and starts giving ticks and render-calls to a scene.
        :return: None
        """
        self.running = True
        if self.scene:
            self.scene.scene_will_start()
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
        if self.scene:
            self.scene.tick(self.ticks)

            self.window.screen.nodelay(True)
            try:
                key_press = self.window.screen.getkey()
                self.scene.key_pressed(key_press)
            except:
                pass

        self.ticks += 1
        if self.ticks >= sys.maxsize:
            self.ticks = 0

    def render(self):
        """
        Renders the screen with appropriate data from current scene.
        Calls render() on the current scene to let it know that we're going to render.
            This might give the scene a chance to do any pre-render actions if necessary.
        :return: None
        """
        if self.scene:
            self.scene.render()

        self.window.clear_screen()

        for game_object in self.scene.objects:
            self.window.draw_text(game_object.sprite, game_object.x, game_object.y)

        self.window.refresh()
