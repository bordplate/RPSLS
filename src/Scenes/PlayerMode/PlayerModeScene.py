from Scene import Scene
from Scenes.PlayerMode.PlayerModeObject import *
import Scenes.Menu.MenuScene
import Scenes.Game.GameScene


class PlayerModeScene(Scene):
    play_modes = [PlayerModeObject(PlayingType.single_player), PlayerModeObject(PlayingType.multiplayer)]

    def scene_will_start(self):
        # Set up both modes correctly on the screen
        self.play_modes[0].x = 2
        self.play_modes[0].y = 2
        self.play_modes[0].set_selected(True)

        self.play_modes[1].x = 40
        self.play_modes[1].y = 2

        # Add both to list of objects
        self.add_objects(self.play_modes)

    def key_pressed(self, key: str):
        super().key_pressed(key)

        if key == "KEY_RIGHT":
            self.play_modes[0].set_selected(False)
            self.rotate_play_modes(1)
        elif key == "KEY_LEFT":
            self.play_modes[0].set_selected(False)
            self.rotate_play_modes(-1)
        elif key == "\n" or key == " ":
            self.play_modes[0].activate()
        elif key == "q":  # User wants to back to menu screen
            self.change_scene(Scenes.Menu.MenuScene.MenuScene())

        self.play_modes[0].set_selected(True)

    def rotate_play_modes(self, times):
        self.play_modes = self.play_modes[times:] + self.play_modes[:times]

    def render(self):
        pass

    def tick(self, ticks):
        pass
