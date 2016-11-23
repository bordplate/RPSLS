from RenderableObject import *


class MenuObject(RenderableObject):
    x = 0
    y = 0
    sprite = ""
    sprite_index = 0
    sprite_frames = []

    selected = False  # If this is the selected menu item
    newly_selected = False

    animation_frequency = 0

    def __init__(self):
        super().__init__()

        self.x = 3
        self.y = 2
        self.sprite = ""
        self.sprite_index = 0
        self.sprite_frames = []

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

    def activate(self):
        pass
