from time import sleep
import sys

from Scene import Scene

EXIT_GAME = False  # If set to True, the tick-loop will quit the game.


class Engine(object):
    """
    Engine responsible for rendering logic and game ticks.
    """
    SLEEP_INTERVAL = 0.0416667  # Gives about 24FPS

    window = None  # type: Window
    running = False

    ticks = 0

    scene = None  # type: Scene

    def __init__(self, window):
        self.window = window

    def start(self):
        """
        Fires up the game engine and starts giving ticks and render-calls to a scene.
        :return: None
        """
        self.running = True

        # Start up first scene in program
        if self.scene:
            self.setup_scene(self.scene)

        self.run()  # Start up the endless loop.

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

        # Pass on ticks to scene, and then scene is responsible for passing that on to all it's sub-objects.
        if self.scene:
            self.scene.tick(self.ticks)

            self.window.screen.nodelay(True)  # Makes our next keyboard-listening event not stall execution
            # noinspection PyBroadException
            try:
                key_press = self.window.screen.getkey()
                self.scene.key_pressed(key_press)
            except:
                # We don't really mind if there is an error, 99% of the time it means the key-stroke buffer is empty.
                #   This is normal behaviour in our case, because of the nodelay-call we're doing.
                pass

        # Wrap around the tick count in case we've been running for too long.
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
        if not self.window.terminal_size_ok():
            self.window.draw_text("Please make your terminal bigger", 0, 0)
            return

        self.window.clear_screen()  # Clean up screen, otherwise we're left with artifacts.

        # Go through all renderable objects in scene and render them on screen.
        for game_object in self.scene.objects:
            self.window.draw_text(game_object.sprite, game_object.x, game_object.y)

    def exit(self):
        """
        Makes the engine cleanly exit the game.
        :return: None
        """
        self.running = False

    def setup_scene(self, scene: Scene):
        """
        Sets up and configures a scene. Will call scene.scene_will_start() when setup has finished.
        :param scene: New scene that will show up.
        :return: None
        """
        scene.change_scene = self.change_scene

        scene.width = self.window.width
        scene.height = self.window.height

        # Finally, tell scene that setup has finished and it can do it's own configuration.
        scene.scene_will_start()

    def change_scene(self, scene: Scene):
        """
        Method that overrides corresponding function in scenes.
        This method changes out the current running scene with a specified one.
        :param scene: New scene to be opened.
        :return: None
        """
        self.setup_scene(scene)
        self.scene = scene
