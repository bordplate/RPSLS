from Scenes.Game.Monsters.Monster import Monster


class Spock(Monster):
    id_mask = int('10000', base=2)
    attack_mask = int('00101', base=2)
