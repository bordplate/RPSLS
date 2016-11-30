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

        if self.x <= 0:
            self.x = self.scene.width - 2
        elif self.x >= self.scene.width - 1:
            self.x = 1
        elif self.y <= 0:
            self.y = self.scene.height - 2
        elif self.y >= self.scene.height - 1:
            self.y = 1
