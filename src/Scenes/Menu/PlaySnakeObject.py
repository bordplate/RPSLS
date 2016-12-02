from Scenes.Menu.MenuObject import MenuObject
from Scenes.Snake.SnakeScene import SnakeScene


class PlaySnakeObject(MenuObject):
    """
    Menu option for starting to play Snake, the bonus feature of this program.
    """
    def __init__(self):
        super().__init__()

        self.x = 69
        self.y = 12

        super().load_sprite('sprites/play-snake.txt')

    def activate(self):
        """

        :return: None
        """
        # Prepare game scene and tell the engine to start it.
        snake_scene = SnakeScene()
        self.scene.change_scene(snake_scene)

        super().activate()
