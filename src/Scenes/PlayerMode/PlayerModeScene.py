from Scene import Scene

from Scenes.PlayerMode.PlayerModeObject import *

import Scenes.Menu.MenuScene
import Scenes.Game.GameScene


class PlayerModeScene(Scene):
    """
    Scene where the user can choose to play either single- or multiplayer.
    """
    play_modes = [PlayerModeObject(PlayingType.single_player), PlayerModeObject(PlayingType.multiplayer)]

    def scene_will_start(self):
        """

        :return:
        """
        # Set up both modes correctly on the screen
        self.play_modes[0].set_position(x=2, y=2)
        self.play_modes[0].set_selected(True)

        self.play_modes[1].set_position(x=40, y=2)
        self.play_modes[1].set_selected(False)

        # Add both to list of objects
        self.add_objects(self.play_modes)

    def key_pressed(self, key: str):
        """
        Switches selection based on user input.
        :param key: Key the user pressed.
        :return: None
        """
        super().key_pressed(key)

        if key == "KEY_RIGHT":
            self.play_modes[0].set_selected(False)
            self.rotate_play_modes(1)
        elif key == "KEY_LEFT":
            self.play_modes[0].set_selected(False)
            self.rotate_play_modes(-1)
        elif key == "\n" or key == " ":  # User wants to activate selected item.
            self.play_modes[0].activate()
        elif key == "q":  # User wants to back to menu screen
            self.change_scene(Scenes.Menu.MenuScene.MenuScene())

        # Just set whatever to active, without caring too much about what keys the user has pressed.
        self.play_modes[0].set_selected(True)

    def rotate_play_modes(self, times: int):
        """
        Rotates the `play_modes' array. Easier to use this than to have an iterator at class-level.
        :param times: Amount of times to shift the array.
        :return: None
        """
        self.play_modes = self.play_modes[times:] + self.play_modes[:times]

    def tick(self, ticks: int):
        """
        Does nothing in this case.
        :param ticks: Current engine tick count
        :return: None
        """
        pass
