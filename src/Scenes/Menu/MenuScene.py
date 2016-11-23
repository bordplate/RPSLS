from Scene import Scene
from Scenes.Menu.PlayGameObject import PlayGameObject
from Scenes.Menu.InstructionsObject import InstructionsObject
from Scenes.Menu.QuitGameObject import QuitGameObject


class MenuScene(Scene):
    objects = []

    menu_items = [PlayGameObject(), InstructionsObject(), QuitGameObject()]

    def render(self):
        pass

    def tick(self, ticks):
        super().tick(ticks)

    def scene_will_start(self):
        self.objects += self.menu_items
        self.menu_items[0].selected = True

    def will_chance_scene(self):
        pass

    def key_pressed(self, key: str):
        super().key_pressed(key)

        if key == "KEY_RIGHT":
            self.menu_items[0].selected = False
            self.rotate_menu_items(1)
        elif key == "KEY_LEFT":
            self.menu_items[0].selected = False
            self.rotate_menu_items(-1)
        elif key == "\n" or key == " ":
            self.menu_items[0].activate()

        self.menu_items[0].selected = True

    def rotate_menu_items(self, times):
        self.menu_items = self.menu_items[times:] + self.menu_items[:times]
