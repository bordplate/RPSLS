from RenderableObject import RenderableObject

from abc import abstractproperty


class Monster(RenderableObject):
    @abstractproperty
    def id_mask(self) -> int:
        pass

    @abstractproperty
    def attack_mask(self) -> int:
        pass

    selected = False
    animation_frequency = 10
    newly_selected = False

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

    def tick(self, ticks):
        if self.selected:
            # Perform a check to see if this item was just selected.
            # This is done to start animating the icon right away, so the user doesn't think the program is frozen.
            if self.newly_selected:
                self.animation_frequency = ticks % 10
                self.newly_selected = False

            # Animate the icon every 10th tick.
            if ticks % 10 == self.animation_frequency:
                self.next_sprite_frame()
        else:
            self.sprite = self.sprite_frames[0]  # Not selected, so just set the icon to first frame,
            # performance penalties too low to care about

        super().tick(ticks)
