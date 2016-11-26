from Scenes.Game.Monsters.Monster import Monster


class Scissors(Monster):
    id_mask = int('00100', base=2)
    attack_mask = int('01010', base=2)
