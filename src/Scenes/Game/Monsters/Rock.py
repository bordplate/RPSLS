from Scenes.Game.Monsters.Monster import Monster
import curses


class Rock(Monster):
    id_mask = int('00001', base=2)
    attack_mask = int('01100', base=2)

    def __init__(self):
        super().__init__()

        self.sprite_style = curses.A_LEFT
