from Scene import Scene
from RenderableObject import RenderableObject

from Scenes.PlayerMode.PlayingType import PlayingType
from Scenes.Game.Hand import Hand
from Scenes.Game.RestartDialog import RestartDialog
from Scenes.Game.Monsters import Rock, Paper, Scissors, Lizard, Spock, Monster

import Scenes.Menu.MenuScene  # Normal import, as a from-import would create recursive imports

from enum import Enum
from copy import copy
from random import randint, choice


# Player that is playing the game.
# The values decide which way to animate the respective characters when they win.
class Player(Enum):
    player1 = 1
    player2 = -1


# Which stage the player(s) are at
class Stage(Enum):
    character_selection = 0  # Player(s) are selecting their characters
    shaking = 1  # Player(s) have chosen, this stage is purely animation (shaking hands)
    announce = 2  # Hand shaking is done, announce winner and explode the loser (explode both if tie)
    restart = 3  # Display restart dialog on screen, so player(s) can choose to restart the game if they want to.


# All characters in the game. Referred to as 'monsters' in the code (some times referred to as characters in comments).
# Monsters in this enum must be a sub-class of `Monster'.
class Monsters(Enum):
    rock = Rock.Rock
    paper = Paper.Paper
    scissors = Scissors.Scissors
    lizard = Lizard.Lizard
    spock = Spock.Spock


class GameScene(Scene):
    """
    This scene is the actual game. Where the player(s) pick characters and see the results.
    The scene consists of 4 main stages:
        1) The player will pick their character, and if it is a multiplayer game, let player 2 pick a character as well.
        2) This is purely for animation. This stage will animate shaking hands, as in a real life game of rock,
                paper, scissors.
        3) This is the announcement stage, where the winner and loser (or a tied game) is announced.
        4) Last stage is just a dialog that prompts the player(s) to restart the game or go back to main menu.
    """
    # What kind of playing type this is (multiplayer / single-player)
    playing_type = None  # type: PlayingType

    # See class-documentation string.
    stage = None  # type: Stage

    # Current player selecting a character
    currently_selecting = None  # type: Player

    # Winner and loser, used in stage 3 and 4 to announce winner.
    winner = None  # type: Player
    loser = None  # type: Player

    # All available monsters, monsters from `Monsters'-enum gets put in here in stage 1 for easier access later on.
    monsters = []

    # Dictionary that tells what player has picked what monster.
    selected_monsters = {}  # type: {}[Player, Monster]

    # This will be set to `True' when stage 3 is done animating so we can show the restart dialog.
    done_announcing = False

    # Restart dialog for stage 4
    restart_dialog = None  # type: RestartDialog

    # Used in stage 1 to tell player(s) whose turn it is to pick a character.
    picking_label = RenderableObject()

    def __init__(self, playing_type: PlayingType):
        """
        Sets the class level `playing_type' variable to specified one.
        :param playing_type: Multiplayer or single-player game.
        """
        super().__init__()

        self.playing_type = playing_type

    def scene_will_start(self):
        """
        Sets stage to the first one (character selection)
        :return: None
        """
        self.set_stage(Stage.character_selection)

    def tick(self, ticks: int):
        """
        Moves the monsters towards each other if we're at the announce-stage.
        :param ticks: Current engine tick count
        :return: None
        """
        super().tick(ticks)

        # We're only doing animation in the announce-stage, and only if we're not done announcing yet.
        if self.stage == Stage.announce and not self.done_announcing:
            if self.winner is None:  # If there is no winner, assume tie and explode both monsters.
                self.selected_monsters[Player.player1].explode(self.monster_explosion_ended)
                self.selected_monsters[Player.player2].explode()

                self.done_announcing = True
            else:  # Move characters until they collide, and then explode the losing character.
                winner_monster = self.selected_monsters[self.winner]
                loser_monster = self.selected_monsters[self.loser]

                if winner_monster.intersects_with(loser_monster):  # Characters have collided.
                    loser_monster.explode(self.monster_explosion_ended)
                    self.done_announcing = True
                else:
                    winner_monster.x += self.winner.value  # Move winning monster towards losing monster

    def key_pressed(self, key: str):
        """
        If we're in character selection, check move selection right or left based on user input.
        If we're in restart section, move selection in the restart dialog.
        :param key: Key that the user pressed.
        :return: None
        """
        super().key_pressed(key)

        if self.stage == Stage.character_selection:  # Get key presses when user is selecting a character
            if key == "KEY_RIGHT":
                self.monsters[0].set_selected(False)
                self.rotate_monsters(1)
                self.monsters[0].set_selected(True)
            elif key == "KEY_LEFT":
                self.monsters[0].set_selected(False)
                self.rotate_monsters(-1)
                self.monsters[0].set_selected(True)
            elif key == "\n" or key == " ":
                self.select_monster(self.currently_selecting, self.monsters[0])
        elif self.stage == Stage.restart:  # Get key presses for the restart dialog.
            if key == "KEY_RIGHT":
                self.restart_dialog.next_selection()
            if key == "KEY_LEFT":
                self.restart_dialog.next_selection()
            if key == "\n" or key == " ":
                if self.restart_dialog.selection == "Yes":
                    self.set_stage(Stage.character_selection)  # Restart the game with same playing type
                else:  # Go back to main menu.
                    menu_scene = Scenes.Menu.MenuScene.MenuScene()
                    self.change_scene(menu_scene)

    def next_selection(self):
        """
        Sets the currently selecting player to next in line, or AI will select monster, if appropriate.
        If player 2 was selecting a character, start next stage.
        :return: None
        """
        if self.currently_selecting == Player.player1:
            self.currently_selecting = Player.player2

            # Randomize which character is animating, so next user "won't see" which character first player picked.
            self.rotate_monsters(randint(0, 4))
            self.monsters[0].set_selected(True)

            if self.playing_type == PlayingType.single_player:  # Single-player came, make "AI" pick character.
                self.select_monster(Player.player2, choice(self.monsters))

            self.picking_label.sprite = "Player 2, it's your turn to pick a character"
        else:  # Both player's must have picked, proceed to next stage.
            self.set_stage(Stage.shaking)

    def select_monster(self, player: Player, monster: Monster):
        """
        Puts selection for a given character into a dictionary for later use.
        :param player: Which player has selected a character.
        :param monster: Which character has been selected.
        :return: None
        """
        monster.set_selected(False)  # Stop animation

        # If we don't copy, any changes to the selected monster is reflected in the selection screen as well.
        self.selected_monsters[player] = copy(monster)

        self.next_selection()

    def reset(self):
        """
        Resets all variables that needs to be set when starting (or restarting) the game.
        :return: None
        """
        self.winner = None
        self.loser = None

        self.selected_monsters = {}
        self.monsters = []

        self.done_announcing = None

        self.restart_dialog = None

        self.currently_selecting = Player.player1  # Player 1 will always start picking

        self.picking_label.set_position(x=3, y=2)
        self.picking_label.sprite = "Player 1, please pick a character"

        self.add_objects([self.picking_label])

    def set_stage(self, stage: Stage):
        """
        Sets up the specified stage
        :param stage: 1 of the 4 stages in the game.
        :return: None
        """
        # We want 3rd stage in background of restart dialog. So don't clean screen if we will be showing restart stage.
        if not stage == Stage.restart:
            self.objects = []  # Clean up objects on screen.

        self.stage = stage

        if stage == Stage.character_selection:
            self.reset()  # First stage means either start of game or restart, so just reset in case.

            i = 0
            for monster_object in Monsters:  # type: Monsters
                monster = monster_object.value
                monster = monster()  # Python wasn't too happy with instantiating on the above line.

                monster.set_position(x=2, y=7)

                # Dynamically add characters to the screen with same spacing between each other.
                if len(self.monsters) > 0:
                    monster.x += self.monsters[i-1].x + self.monsters[i-1].width

                self.add_objects([monster])
                self.monsters += [monster]

                i += 1

            self.monsters[0].set_selected(True)
        elif stage == Stage.shaking:  # Add a left and a right hand to the screen and "shake" them.
            screen_center = int(self.width / 2)

            # Add shaking hands to screen
            hand_left = Hand()
            hand_right = Hand()

            # If one hand has stopped animating, assume both have
            hand_left.animation_did_end = self.hand_stopped_animating  # Add callback method.

            # Try to center both hands on the screen.
            hand_left.set_position(x=screen_center - hand_left.width - 10, y=5)

            hand_right.set_position(x=screen_center+10, y=5)
            hand_right.flip_sprite()

            self.add_objects([hand_left, hand_right])

            hand_left.start_animating()
            hand_right.start_animating()
        elif stage == Stage.announce:  # Stage where winner and loser is announced.
            screen_center = int(self.width / 2)

            player1_monster = self.selected_monsters[Player.player1]  # type: Monster
            player2_monster = self.selected_monsters[Player.player2]  # type: Monster

            # Center the characters and then mirror player 2's sprite.
            player1_monster.set_position(x=screen_center-player1_monster.width-10, y=5)

            player2_monster.set_position(x=screen_center+10, y=5)
            player2_monster.flip_sprite()

            # Compare player 1 and player 2 defence- and attack-mask.
            player1_attack = player2_monster.id_mask & player1_monster.attack_mask
            player2_attack = player1_monster.id_mask & player2_monster.attack_mask

            # If an attack yields a value over 0, it means that attack wins. If none yield result over 0, that's a tie.
            if player1_attack > 0:
                self.winner = Player.player1
                self.loser = Player.player2
            elif player2_attack > 0:
                self.winner = Player.player2
                self.loser = Player.player1
            else:
                self.winner = None  # winner: None, implies a tie.

            self.add_objects([player1_monster, player2_monster])
        elif stage == Stage.restart:  # Stage where a restart dialog appears, so user can choose to restart or not.
            # Enum value of `Player' is for animation, so we have to "manually" if-else here.
            if self.winner == Player.player1:
                self.restart_dialog = RestartDialog(winner=1)
            elif self.winner == Player.player2:
                self.restart_dialog = RestartDialog(winner=2)
            else:
                self.restart_dialog = RestartDialog(winner=3)

            self.restart_dialog.set_position(x=20, y=5)

            self.add_objects([self.restart_dialog])

    def rotate_monsters(self, times):
        """
        Used to shift the monsters-array around, instead of having an iterator at the top of the class.
        :param times: Times to shift the array.
        :return: None
        """
        self.monsters = self.monsters[times:] + self.monsters[:times]

    def hand_stopped_animating(self):
        """
        Callback method for when a character has stopped animating.
        :return: None
        """
        self.set_stage(Stage.announce)

    def monster_explosion_ended(self):
        """
        Callback method for when an explosion has ended.
        :return: None
        """
        self.set_stage(Stage.restart)
