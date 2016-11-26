from RenderableObject import RenderableObject

from Scenes.PlayerMode.PlayingType import PlayingType
from Scenes.Game.GameScene import GameScene


class PlayerModeObject(RenderableObject):
    selected = False

    playing_type = None  # type: PlayingType

    def __init__(self, playing_type: PlayingType):
        """
        Inits the object and sets the selection type for this object.
        :param playing_type: A string as PlayingType
        """
        super().__init__()

        self.playing_type = playing_type

        # noinspection PyTypeChecker
        self.load_sprite("sprites/play-" + playing_type.value + ".txt")

    def set_selected(self, value: bool):
        self.selected = value
        if value:
            self.sprite = self.sprite_frames[1]
        else:
            self.sprite = self.sprite_frames[0]

    def activate(self):
        game_scene = GameScene(self.playing_type)
        self.scene.change_scene(game_scene)
