from RenderableObject import RenderableObject


class Hand(RenderableObject):
    def __init__(self):
        super().__init__()

        self.load_sprite("sprites/hand.txt")

    animating = False
    move_count = 0
    movement = 1

    def start_animating(self):
        self.animating = True

    def animation_did_end(self):
        pass

    def tick(self, ticks):
        super().tick(ticks)

        if self.animating and ticks % 5 == 0:
            self.y += self.movement

            self.move_count += 1

            if 3 <= self.move_count < 6:
                self.movement = -1
            elif 6 <= self.move_count < 9:
                self.movement = 1
            elif self.move_count >= 9:
                self.animating = False
                self.animation_did_end()
