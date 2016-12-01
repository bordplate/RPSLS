from Scenes.Menu.MenuObject import MenuObject
from Scenes.Snake.SnakeScene import SnakeScene


class PlaySnakeObject(MenuObject):
    sprite = ""
    sprite_index = 0
    sprite_frames = []

    x = 0
    y = 0

    def __init__(self):
        super().__init__()

        self.x = 69
        self.y = 12
        self.sprite = ""
        self.sprite_index = 0
        self.sprite_frames = []

        super().load_sprite('sprites/play-snake.txt')

    def activate(self):
        # Prepare game scene and tell the engine to start it.
        snake_scene = SnakeScene()
        self.scene.change_scene(snake_scene)
