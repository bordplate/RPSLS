from Scenes.Menu.MenuObject import *
import Engine  # A bit nasty, but seems to be the cleanest way to do this


class QuitGameObject(MenuObject):
    """
    Quits the game when activated.
    """
    def __init__(self):
        """
        Sets the position for this menu option.
        """
        super().__init__()

        self.x = 50
        self.y = 12

        super().load_sprite('sprites/quit-game.txt')

    def activate(self):
        """
        Sets the engine's exit-game variable to true, which in turn makes it stop it's run-loop.
        :return: None
        """
        Engine.EXIT_GAME = True

        super().activate()
