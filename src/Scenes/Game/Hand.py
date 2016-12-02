from RenderableObject import RenderableObject


class Hand(RenderableObject):
    """
    An animatable hand, used for animating the shaking-stage of Rock, Paper, Scissors, Lizard, Spock
    """
    def __init__(self):
        """
        Loads the sprite for the hand.
        """
        super().__init__()

        self.load_sprite("sprites/hand.txt")

    animating = False
    move_count = 0  # How many "pixels" the hand has moved
    movement = 1  # 1 if it should move down, -1 if it should move up

    def start_animating(self):
        """
        Starts animating the hands.
        :return: None
        """
        self.animating = True

    def animation_did_end(self):
        """
        Callback that this object calls when it has finished animating.
        :return: None
        """
        pass

    def tick(self, ticks: int):
        """
        Moves the hand every 5 ticks.
        Moves the hand up or down depending on how far in the animation cycle it has come.
        Starts up with moving down, then moves up and then down again.
        :param ticks: Current engine tick count
        :return: None
        """
        super().tick(ticks)

        if self.animating and ticks % 5 == 0:
            self.y += self.movement

            self.move_count += 1

            if 3 <= self.move_count < 6:  # Start moving hand up again
                self.movement = -1
            elif 6 <= self.move_count < 9:  # Start moving hand down again
                self.movement = 1
            elif self.move_count >= 9:  # Animation is done.
                self.animating = False
                self.animation_did_end()
