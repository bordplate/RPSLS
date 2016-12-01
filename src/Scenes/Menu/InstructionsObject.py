from Scenes.Menu.MenuObject import *

from Scenes.Instructions.InstructionsScene import InstructionsScene

class InstructionsObject(MenuObject):
    sprite = ""
    sprite_index = 0
    sprite_frames = []

    x = 0
    y = 0

    def __init__(self):
        super().__init__()

        self.x = 26
        self.y = 12
        self.sprite = ""
        self.sprite_index = 0
        self.sprite_frames = []

        super().load_sprite('sprites/open-instructions.txt')

    def activate(self):
        super().activate()

        self.scene.change_scene(InstructionsScene())
