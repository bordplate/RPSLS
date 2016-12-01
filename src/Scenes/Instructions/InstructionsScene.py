from Scene import Scene
from RenderableObject import RenderableObject

import Scenes.Menu.MenuScene


class InstructionsScene(Scene):
    instructions = None  # type: RenderableObject

    def scene_will_start(self):
        self.instructions = RenderableObject()

        self.instructions.load_sprite("sprites/instructions.txt")

        self.instructions.x = int(self.width / 2) - int(self.instructions.width / 2)
        self.instructions.y = int(self.height / 2) - int(self.instructions.height / 2)

        self.add_objects([self.instructions])

    def key_pressed(self, key: str):
        if key == "q":
            self.change_scene(Scenes.Menu.MenuScene.MenuScene())

    def render(self):
        pass

    def tick(self, ticks):
        pass
