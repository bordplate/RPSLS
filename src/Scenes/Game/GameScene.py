from Scene import Scene
from RenderableObject import RenderableObject

from Scenes.PlayerMode.PlayingType import PlayingType
from Scenes.Game.Hand import Hand
from Scenes.Game.RestartDialog import RestartDialog
from Scenes.Game.Monsters import Rock, Paper, Scissors, Lizard, Spock, Monster

import Scenes.Menu.MenuScene

from enum import Enum
from copy import copy
from random import randint, choice


class Player(Enum):
    player1 = 1
    player2 = -1


class Stage(Enum):
    character_selection = 0
    shaking = 1
    announce = 2
    restart = 3


class Monsters(Enum):
    rock = Rock.Rock
    paper = Paper.Paper
    scissors = Scissors.Scissors
    lizard = Lizard.Lizard
    spock = Spock.Spock


class GameScene(Scene):
    playing_type = None  # type: PlayingType

    stage = None  # type: Stage

    currently_selecting = None  # type: Player
    winner = None  # type: Player
    loser = None  # type: Player

    monsters = []
    selected_monsters = {}  # type: {}[Player, Monster]

    done_announcing = False

    restart_dialog = None  # type: RestartDialog

    picking_label = RenderableObject()

    def __init__(self, playing_type: PlayingType):
        super().__init__()

        self.playing_type = playing_type

    def scene_will_start(self):
        self.set_stage(Stage.character_selection)

    def tick(self, ticks):
        super().tick(ticks)

        if self.stage == Stage.announce and not self.done_announcing:
            if self.winner is None:  # If there is no winner, assume tie.
                self.selected_monsters[Player.player1].explode(self.monster_explosion_ended)
                self.selected_monsters[Player.player2].explode()
                self.done_announcing = True
            else:
                winner_monster = self.selected_monsters[self.winner]
                loser_monster = self.selected_monsters[self.loser]

                if winner_monster.intersects_with(loser_monster):
                    loser_monster.explode(self.monster_explosion_ended)
                    self.done_announcing = True
                else:
                    winner_monster.x += self.winner.value

    def key_pressed(self, key: str):
        super().key_pressed(key)

        if self.stage == Stage.character_selection:
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
        elif self.stage == Stage.restart:
            if key == "KEY_RIGHT":
                self.restart_dialog.next_selection()
            if key == "KEY_LEFT":
                self.restart_dialog.next_selection()
            if key == "\n" or key == " ":
                if self.restart_dialog.selection == "Yes":
                    self.set_stage(Stage.character_selection)
                else:
                    menu_scene = Scenes.Menu.MenuScene.MenuScene()
                    self.change_scene(menu_scene)

    def next_selection(self):
        """
        Sets the currently selecting player to next in line, or AI will select monster, if appropriate.
        :return: None
        """
        if self.currently_selecting == Player.player1:
            self.currently_selecting = Player.player2

            self.rotate_monsters(randint(0, 4))  # Randomize selection for next user
            self.monsters[0].set_selected(True)

            if self.playing_type == PlayingType.single_player:
                self.select_monster(Player.player2, choice(self.monsters))  # Make AI pick a monster

            self.picking_label.sprite = "Player 2, it's your turn to pick a character"
        else:
            self.set_stage(Stage.shaking)

    def select_monster(self, player: Player, monster: Monster):
        """

        :param player:
        :param monster:
        :return:
        """
        monster.set_selected(False)  # Stop animation
        self.selected_monsters[player] = copy(monster)
        self.next_selection()

    def set_stage(self, stage: Stage):
        """
        Sets up the specified stage
        :param stage:
        :return: None
        """
        # We want the restart dialog over the last stage. So don't clean screen if we will be showing restart stage.
        if not stage == Stage.restart:
            self.objects = []  # Clean up objects on screen.

        self.stage = stage

        if stage == Stage.character_selection:
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

            i = 0
            for monster_object in Monsters:  # type: Monsters
                monster = monster_object.value
                monster = monster()  # Python wasn't too happy with instantiating on the above line.

                monster.y = 7
                monster.x = 2

                if len(self.monsters) > 0:
                    monster.x += self.monsters[i-1].x + self.monsters[i-1].width

                self.add_objects([monster])
                self.monsters += [monster]

                i += 1

            self.monsters[0].set_selected(True)
        elif stage == Stage.shaking:
            screen_center = int(self.width / 2)

            # Add shaking hands to screen
            hand_left = Hand()
            hand_right = Hand()

            hand_left.set_position(x=screen_center-hand_left.width-10, y=5)

            # If one hand has stopped animating, assume both have
            hand_left.animation_did_end = self.hand_stopped_animating

            hand_right.set_position(x=screen_center+10, y=5)
            hand_right.flip_sprite()

            self.add_objects([hand_left, hand_right])

            hand_left.start_animating()
            hand_right.start_animating()
        elif stage == Stage.announce:
            screen_center = int(self.width / 2)

            player1_monster = self.selected_monsters[Player.player1]  # type: Monster
            player2_monster = self.selected_monsters[Player.player2]  # type: Monster

            player1_monster.set_position(x=screen_center-player1_monster.width-10, y=5)

            player2_monster.set_position(x=screen_center+10, y=5)
            player2_monster.flip_sprite()

            player1_attack = player2_monster.id_mask & player1_monster.attack_mask
            player2_attack = player1_monster.id_mask & player2_monster.attack_mask

            if player1_attack > 0:
                self.winner = Player.player1
                self.loser = Player.player2
            elif player2_attack > 0:
                self.winner = Player.player2
                self.loser = Player.player1
            else:
                self.winner = None

            self.add_objects([player1_monster, player2_monster])
        elif stage == Stage.restart:
            if self.winner == Player.player1:
                self.restart_dialog = RestartDialog(winner=1)
            elif self.winner == Player.player2:
                self.restart_dialog = RestartDialog(winner=2)
            else:
                self.restart_dialog = RestartDialog(winner=3)

            self.restart_dialog.set_position(x=20, y=5)

            self.add_objects([self.restart_dialog])

    def render(self):
        pass

    def rotate_monsters(self, times):
        self.monsters = self.monsters[times:] + self.monsters[:times]

    def hand_stopped_animating(self):
        self.set_stage(Stage.announce)

    def monster_explosion_ended(self):
        self.set_stage(Stage.restart)
