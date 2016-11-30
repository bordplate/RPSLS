from Scenes.Game.Monsters.Monster import Monster


class Rock(Monster):
    id_mask = int('00001', base=2)
    attack_mask = int('01100', base=2)
