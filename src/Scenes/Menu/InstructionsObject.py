from Scenes.Menu.MenuObject import *

from Scenes.Instructions.InstructionsScene import InstructionsScene

class InstructionsObject(MenuObject):
    """
    Menu option for displaying instructions on screen when activated.
    """
    def __init__(self):
        """
        Sets the position for this menu object and laods it's sprite
        """
        super().__init__()

        self.x = 26
        self.y = 12

        super().load_sprite('sprites/open-instructions.txt')

    def activate(self):
        """
        Opens the instructions when activated.
        :return: None
        """
        super().activate()

        self.scene.change_scene(InstructionsScene())
