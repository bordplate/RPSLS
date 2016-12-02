from Scene import Scene
from RenderableObject import RenderableObject

# Import all of the menu options.
from Scenes.Menu.PlayGameObject import PlayGameObject
from Scenes.Menu.InstructionsObject import InstructionsObject
from Scenes.Menu.QuitGameObject import QuitGameObject
from Scenes.Menu.PlaySnakeObject import PlaySnakeObject


class MenuScene(Scene):
    """
    Displays a menu with all game options available.
    """
    menu_items = [PlayGameObject(), InstructionsObject(), QuitGameObject(), PlaySnakeObject()]

    def tick(self, ticks: int):
        """
        Does nothing in this case. Only calls super's tick-method.
        :param ticks: Current engine tick count
        :return: None
        """
        super().tick(ticks)

    def scene_will_start(self):
        """
        Adds all available objects to the screen.
        :return: None
        """
        self.add_objects(self.menu_items)
        self.menu_items[0].selected = True  # Activate the first menu item.

        # Add title to top of the menu.
        menu_text = RenderableObject()
        menu_text.load_sprite("sprites/menu_text.txt")

        menu_text.y = 4
        menu_text.x = int(self.width / 2) - int(menu_text.width / 2)  # Center the menu.

        self.add_objects([menu_text])

    def key_pressed(self, key: str):
        """
        Checks if the user is navigating the menu or selecting an item.
        :param key: Key the user pressed.
        :return: None
        """
        if key == "KEY_RIGHT":
            self.menu_items[0].set_selected(False)
            self.rotate_menu_items(1)
        elif key == "KEY_LEFT":
            self.menu_items[0].set_selected(False)
            self.rotate_menu_items(-1)
        elif key == 'q':
            QuitGameObject().activate()  # Easier to do this than the ugly Engine-importing trick

        # Always set current menu item to selected, to avoid doing it explicitly in right, left checking code.
        self.menu_items[0].set_selected(True)

        # We check these keys here because other wise when we're setting the menu item to selected above, it's
        #   selecting the option again right after the item has tried to unselect itself.
        if key == "\n" or key == " ":
            self.menu_items[0].activate()

    def rotate_menu_items(self, times):
        """
        Roates the menu items.
        We're doing this so we don't need to have a menu iterator at the top-level of the class.
        :param times: Amount of times to rotate/shift the menu options.
        :return: None
        """
        self.menu_items = self.menu_items[times:] + self.menu_items[:times]
