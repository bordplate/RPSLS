from Scene import Scene

from Scenes.PlayerMode.PlayingType import PlayingType
from Scenes.Game.Monsters import Rock, Paper, Scissors, Lizard, Spock, Monster
from RenderableObject import RenderableObject

from enum import Enum


class Player(Enum):
    player1 = 0
    player2 = 1


class Stage(Enum):
    character_selection = 0
    shaking = 1
    announce = 2


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

    monsters = []
    selected_monsters = {}  # type: {}[Player, Monster]

    def __init__(self, playing_type: PlayingType):
        super().__init__()

        self.playing_type = playing_type

    def scene_will_start(self):
        self.set_stage(Stage.character_selection)

    def tick(self, ticks):
        super().tick(ticks)

        if self.stage == Stage.character_selection:
            pass

    def key_pressed(self, key: str):
        super().key_pressed(key)

        if self.stage == Stage.character_selection:
            if key == "KEY_RIGHT":
                self.monsters[0].set_selected(False)
                self.rotate_monsters(1)
            elif key == "KEY_LEFT":
                self.monsters[0].set_selected(False)
                self.rotate_monsters(-1)
            elif key == "\n" or key == " ":
                self.select_monster(self.currently_selecting, self.monsters[0])

            self.monsters[0].set_selected(True)

    def next_selection(self):
        """
        Sets the currently selecting player to next in line.
        :return: None
        """
        if self.currently_selecting == Player.player1:
            self.currently_selecting = Player.player2

            if self.playing_type == PlayingType.single_player:
                self.select_monster(Player.player2, Spock.Spock())  # Make AI pick a monster
        else:
            self.set_stage(Stage.shaking)

    def select_monster(self, player: Player, monster: Monster):
        """

        :param player:
        :param monster:
        :return:
        """
        self.selected_monsters[player] = monster
        self.next_selection()

    def set_stage(self, stage: Stage):
        """
        Sets up the specified stage
        :param stage:
        :return: None
        """
        self.objects = []  # Clean up objects on screen.
        self.stage = stage

        if stage == Stage.character_selection:
            self.currently_selecting = Player.player1  # Player 1 will always start picking

            i = 0
            for monster_object in Monsters:  # type: Monsters
                monster = monster_object.value
                monster = monster()  # Python wasn't too happy with instantiating on the above line.

                monster.y = 2
                monster.x = 2 + (20 * i)

                self.add_objects([monster])
                self.monsters += [monster]

                i += 1

            self.monsters[0].set_selected(True)
        elif stage == Stage.shaking:
            self.set_stage(Stage.announce)
        elif stage == Stage.announce:
            screen_text = RenderableObject()

            player1_monster = self.selected_monsters[Player.player1]  # type: Monster
            player2_monster = self.selected_monsters[Player.player2]  # type: Monster

            attack1 = player2_monster.id_mask & player1_monster.attack_mask
            attack2 = player1_monster.id_mask & player2_monster.attack_mask

            if attack1 > 0 and attack2 == 0:
                screen_text.sprite = "Player 1 wins!"
            elif attack2 > 0 and attack1 == 0:
                screen_text.sprite = "Player 2 wins!"
            else:
                screen_text.sprite = "That's a tie!"

            self.add_objects([screen_text])
        else:
            quit("Dude what")

    def render(self):
        pass

    def rotate_monsters(self, times):
        self.monsters = self.monsters[times:] + self.monsters[:times]
