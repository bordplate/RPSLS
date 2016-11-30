from RenderableObject import RenderableObject

from Scenes.Snake.Direction import Direction


class SnakeTail(RenderableObject):
    direction = Direction.right

    def __init__(self, direction: Direction):
        super().__init__()

        self.set_direction(direction)

    def set_direction(self, direction: Direction):
        self.direction = direction

        if direction == Direction.up or direction == Direction.down:
            self.sprite = "|"
        else:
            self.sprite = "-"

    def tick(self, ticks):
        super().tick(ticks)