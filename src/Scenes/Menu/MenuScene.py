from Scene import Scene
from RenderableObject import RenderableObject

from Scenes.Menu.PlayGameObject import PlayGameObject
from Scenes.Menu.InstructionsObject import InstructionsObject
from Scenes.Menu.QuitGameObject import QuitGameObject
from Scenes.Menu.PlaySnakeObject import PlaySnakeObject


class MenuScene(Scene):
    menu_items = [PlayGameObject(), InstructionsObject(), QuitGameObject(), PlaySnakeObject()]

    def render(self):
        pass

    def tick(self, ticks):
        super().tick(ticks)

    def scene_will_start(self):
        self.add_objects(self.menu_items)
        self.menu_items[0].selected = True  # Activate the first menu item.

        menu_text = RenderableObject()
        menu_text.load_sprite("sprites/menu_text.txt")

        menu_text.y = 4
        menu_text.x = int(self.width / 2) - int(menu_text.width / 2)

        self.add_objects([menu_text])

    def will_change_scene(self):
        pass

    def key_pressed(self, key: str):
        super().key_pressed(key)

        if key == "KEY_RIGHT":
            self.menu_items[0].set_selected(False)
            self.rotate_menu_items(1)
        elif key == "KEY_LEFT":
            self.menu_items[0].set_selected(False)
            self.rotate_menu_items(-1)
        elif key == 'q':
            QuitGameObject().activate()  # Easier to do this than the ugly Engine-importing trick

        self.menu_items[0].set_selected(True)

        if key == "\n" or key == " ":
            self.menu_items[0].activate()

    def rotate_menu_items(self, times):
        self.menu_items = self.menu_items[times:] + self.menu_items[:times]
