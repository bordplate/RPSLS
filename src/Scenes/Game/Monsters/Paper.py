from Scenes.Game.Monsters.Monster import Monster


class Paper(Monster):
    id_mask = int('00010', base=2)
    attack_mask = int('10001', base=2)
