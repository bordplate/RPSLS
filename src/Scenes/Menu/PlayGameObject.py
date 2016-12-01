from Scenes.Menu.MenuObject import MenuObject
from Scenes.PlayerMode.PlayerModeScene import PlayerModeScene


class PlayGameObject(MenuObject):
    sprite = ""
    sprite_index = 0
    sprite_frames = []

    x = 0
    y = 0

    def __init__(self):
        super().__init__()

        self.x = 4
        self.y = 12
        self.sprite = ""
        self.sprite_index = 0
        self.sprite_frames = []

        super().load_sprite('sprites/play-game.txt')

    def activate(self):
        # Prepare game scene and tell the engine to start it.
        player_mode_scene = PlayerModeScene()
        self.scene.change_scene(player_mode_scene)
