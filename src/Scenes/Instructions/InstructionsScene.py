from Scene import Scene
from RenderableObject import RenderableObject

import Scenes.Menu.MenuScene


class InstructionsScene(Scene):
    """
    A scene that shows game instructions to the user.
    """
    instructions = None  # type: RenderableObject

    def scene_will_start(self):
        """
        Loads the instructions from a sprite to a renderable object.
        :return: None
        """
        self.instructions = RenderableObject()

        self.instructions.load_sprite("sprites/instructions.txt")

        # Center the instructions on the screen.
        self.instructions.x = int(self.width / 2) - int(self.instructions.width / 2)
        self.instructions.y = int(self.height / 2) - int(self.instructions.height / 2)

        self.add_objects([self.instructions])

    def key_pressed(self, key: str):
        """
        Checks if user wants to quit to menu.
        :param key: Key the user pressed.
        :return: None
        """
        if key == "q":
            self.change_scene(Scenes.Menu.MenuScene.MenuScene())

    def tick(self, ticks: int):
        """
        Does nothing in this case.
        :param ticks: Tick count
        :return: None
        """
        pass
