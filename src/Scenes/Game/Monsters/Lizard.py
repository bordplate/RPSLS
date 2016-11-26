from Scenes.Game.Monsters.Monster import Monster


class Lizard(Monster):
    id_mask = int('01000', base=2)
    attack_mask = int('10010', base=2)
