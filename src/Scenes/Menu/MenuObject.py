from RenderableObject import RenderableObject


class MenuObject(RenderableObject):
    selected = False  # If this is the selected menu item
    newly_selected = False

    animation_frequency = 0

    def __init__(self):
        """
        Sets the standard x,y-position on initiation.
        """
        super().__init__()

        self.x = 3
        self.y = 2

    def set_selected(self, value: bool):
        """
        Sets this object to the specified value and starts animating
        Sets self.newly_selected to true, if it should start animating.
            This makes us able to start animating first tick after it has been selected.
        :param value: Whether or not this object is selected.
        :return: None
        """
        self.selected = value
        self.newly_selected = value

    def tick(self, ticks: int):
        """
        Animtes the icon if appropriate.
        :param ticks: Engine tick count
        :return: None
        """
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
            # Performance penalties too low to care about

        super().tick(ticks)

    def activate(self):
        """
        Overridden in sub-classes. This method is called when a menu object is activated (e.g. user pressed enter)
        Sets itself to false, so it stops animating.
        :return: None
        """
        self.set_selected(False)
