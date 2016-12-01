from Scenes.Menu.MenuObject import *
import Engine  # A bit nasty, but seems to be the cleanest way to do this


class QuitGameObject(MenuObject):
    sprite = ""
    sprite_index = 0
    sprite_frames = []

    x = 0
    y = 0

    def __init__(self):
        super().__init__()

        self.x = 50
        self.y = 12
        self.sprite = ""
        self.sprite_index = 0
        self.sprite_frames = []

        super().load_sprite('sprites/quit-game.txt')

    def activate(self):
        Engine.EXIT_GAME = True

        super().activate()
