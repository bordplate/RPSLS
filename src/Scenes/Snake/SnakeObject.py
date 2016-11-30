from RenderableObject import RenderableObject

from Scenes.Snake.Direction import Direction
from Scenes.Snake.SnakeTail import SnakeTail


class SnakeObject(RenderableObject):
    tail = []

    movement_stack = [Direction.right]

    direction = Direction.right

    halt_tail = False

    def __init__(self):
        super().__init__()

        self.x = 1
        self.y = 2

        self.sprite = ">"

    def set_direction(self, direction: Direction):
        self.direction = direction

        if direction == Direction.up:
            self.sprite = "^"
        elif direction == Direction.down:
            self.sprite = "V"
        elif direction == Direction.left:
            self.sprite = "<"
        elif direction == Direction.right:
            self.sprite = ">"

    def add_tail_part(self):
        tail_part = SnakeTail(self.direction)
        tail_part.set_position(self.x, self.y)

        self.tail.insert(0, tail_part)
        self.scene.add_objects([tail_part])

        self.halt_tail = True

    def tick(self, ticks):
        super().tick(ticks)

        if ticks % 2 == 0:
            self.movement_stack += [self.direction]

            if self.direction == Direction.right:
                self.x += 1
            elif self.direction == Direction.left:
                self.x -= 1
            elif self.direction == Direction.up:
                self.y -= 1
            elif self.direction == Direction.down:
                self.y += 1

            if not self.halt_tail:
                for i, tail_part in enumerate(self.tail):
                    direction = self.movement_stack[-(i+2)]

                    if direction == Direction.right:
                        tail_part.x += 1
                    elif direction == Direction.left:
                        tail_part.x -= 1
                    elif direction == Direction.up:
                        tail_part.y -= 1
                    elif direction == Direction.down:
                        tail_part.y += 1

                    tail_part.set_direction(direction)
            else:
                self.halt_tail = False

            self.movement_stack = self.movement_stack[-len(self.tail):]  # Shave off unnecessary overhead. For memory.

            if self.x <= 0:
                self.x = self.scene.width - 2
            elif self.x >= self.scene.width - 1:
                self.x = 1
            elif self.y <= 0:
                self.y = self.scene.height - 2
            elif self.y >= self.scene.height - 1:
                self.y = 1
