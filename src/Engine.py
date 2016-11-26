from time import sleep
import sys

from Scene import Scene

EXIT_GAME = False  # If set to True, the tick-loop will quit the game.


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
            self.setup_scene(self.scene)
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
        if EXIT_GAME:  # We have to cheat a little to have less friction just to exit the game.
            self.exit()

        if self.scene:
            self.scene.tick(self.ticks)

            self.window.screen.nodelay(True)  # Makes our next keyboard-listening event not stall execution
            # noinspection PyBroadException
            try:
                key_press = self.window.screen.getkey()
                self.scene.key_pressed(key_press)
            except:  # If there is no input, we don't really care.
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

        self.window.clear_screen()  # Clean up screen, otherwise we're left with artifacts.

        # Go through all renderable objects in scene and render them on screen.
        for game_object in self.scene.objects:
            self.window.draw_text(game_object.sprite, game_object.x, game_object.y, game_object.sprite_style)

    def exit(self):
        """
        Cleanly exits the game.
        :return: None
        """
        self.running = False

    def setup_scene(self, scene: Scene):
        scene.scene_will_start()
        scene.change_scene = self.change_scene

    def change_scene(self, scene: Scene):
        self.setup_scene(scene)
        self.scene = scene
