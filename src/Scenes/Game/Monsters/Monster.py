from RenderableObject import RenderableObject

from abc import abstractproperty


class Monster(RenderableObject):
    """
    Selectable character that players can pick.
    Inherit this class to create a new monster, this class should not start up by it's own.

    All monsters have their own "id" bitmask that is their line of defense, e.g. 00100
    All monsters also have their own "attack" bitmask that they use when "attacking" other monsters, e.g. 10100

    The idea is to check if one monster's attack "flips" the bits in another monster's "id". If the ID-bit flips,
        that monster is dead.
    The actual implementation is a bit different.
    """

    # id_mask and attack_mask are must have in inherited classes, and basically the only thing they need.
    # id_mask should only have 1 bit set. attack_mask should have 2 bits set, which should "overwrite"

    @abstractproperty
    def id_mask(self) -> int:
        pass

    @abstractproperty
    def attack_mask(self) -> int:
        pass

    selected = False
    animation_frequency = 10
    newly_selected = False

    exploding = False

    # Defining the callback function as a variable here suppresses Pycharm warnings.
    explosion_animation_did_end = None  # type: def

    def __init__(self):
        super().__init__()

        self.load_sprite("sprites/monsters/" + type(self).__name__ + ".txt")

    def set_selected(self, value: bool):
        """
        Sets this object to the specified value and starts animating
        :param value: Wether or not to be selected.
        :return: None
        """
        self.selected = value
        self.newly_selected = value

        if not value:
            self.sprite = self.sprite_frames[0]

    def explode(self, callback=lambda: None):
        """
        Explodes the sprite.
        :param callback: Defaults to lambda: None, so we never have to check if the callback has a value.
        :return: None
        """
        self.load_sprite("sprites/explosion.txt")
        self.exploding = True
        self.explosion_animation_did_end = callback

    def tick(self, ticks: int):
        if self.selected:
            # Perform a check to see if this item was just selected.
            # This is done to start animating the icon right away, so the user doesn't think the program is frozen.
            if self.newly_selected:
                self.animation_frequency = ticks % 10
                self.newly_selected = False

            # Animate the icon every 10th tick.
            if ticks % 10 == self.animation_frequency:
                self.next_sprite_frame()

        if self.exploding:
            if self.sprite_index >= len(self.sprite_frames)-2:
                self.exploding = False
                self.sprite = ""

                self.explosion_animation_did_end()

            if ticks % 3:
                self.next_sprite_frame()

        super().tick(ticks)
