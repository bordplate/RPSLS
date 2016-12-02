from RenderableObject import RenderableObject

from Scenes.PlayerMode.PlayingType import PlayingType
from Scenes.Game.GameScene import GameScene


class PlayerModeObject(RenderableObject):
    """
    An option in the PlayerModeScene menu. Can be either single- or multiplayer option, based on specified `PlayingType'
    """
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
        """
        Sets this object to selected or not, adds a border (from it's sprite) if appropriate.
        :param value: True if selected, False if not selected.
        :return: None
        """
        self.selected = value
        if value:
            self.sprite = self.sprite_frames[1]
        else:
            self.sprite = self.sprite_frames[0]

    def activate(self):
        """
        User has selected this option, so go along and start the game.
        :return: None
        """
        game_scene = GameScene(self.playing_type)
        self.scene.change_scene(game_scene)
