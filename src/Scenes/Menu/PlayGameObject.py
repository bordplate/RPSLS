from Scenes.Menu.MenuObject import MenuObject
from Scenes.PlayerMode.PlayerModeScene import PlayerModeScene


class PlayGameObject(MenuObject):
    """
    Menu option for starting to play a game of Rock, Paper, Scissors, Lizard, Spock.
    """
    def __init__(self):
        super().__init__()

        self.x = 4
        self.y = 12

        super().load_sprite('sprites/play-game.txt')

    def activate(self):
        """
        Starts the next scene, which is where the player(s) choose to play single- or mulitplayer.
        :return:
        """
        # Prepare game scene and tell the engine to start it.
        player_mode_scene = PlayerModeScene()
        self.scene.change_scene(player_mode_scene)

        super().activate()
