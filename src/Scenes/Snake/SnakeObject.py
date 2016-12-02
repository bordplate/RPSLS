from RenderableObject import RenderableObject

from Scenes.Snake.Direction import Direction
from Scenes.Snake.SnakeTail import SnakeTail


class SnakeObject(RenderableObject):
    """
    Snake's head. Snake moves around on the screen and wraps around if he meets wall.
    Snake keeps a stack of movements he has done, so that all parts of the tail can follow.
    """
    # All tail parts belonging to this instance of Snake.
    tail = []  # type: [TailPart]

    # All movements Snake has done.
    movement_stack = [Direction.right]

    direction = Direction.right  # Direction Snake is taking

    halt_tail = False  # If the tail should stop moving for a tick or two.

    def __init__(self):
        super().__init__()

        self.set_position(x=2, y=1)

        # Reset tail and movement stack in case these hold some values related to an earlier instance of it.
        self.tail = []
        self.movement_stack = [Direction.right]

        self.sprite = ">"

    def set_direction(self, direction: Direction):
        """
        Switches out the "sprite" for the head, depending on the new direction.
        :param direction: Which direction Snake should be facing now.
        :return: None
        """
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
        """
        Adds another part to Snake's tail.
        Halts the rest of the tail for the next tick.
        :return: None
        """
        tail_part = SnakeTail(self.direction)
        tail_part.set_position(self.x, self.y)

        self.tail.insert(0, tail_part)  # We want this part to be at the top of the tail
        self.scene.add_objects([tail_part])

        self.halt_tail = True  # Halt the tail, so Snake can move ahead of it.

    def tick(self, ticks: int):
        """
        Moves Snake and the rest of his tail.
        Wraps Snake around if he goes to a wall.
        :param ticks: The current engine tick count.
        :return: None
        """
        super().tick(ticks)

        # If the game is over, we don't need to do anything.
        if self.scene.game_over:
            return

        # Only move every other tick.
        if ticks % 2 == 0:
            self.movement_stack += [self.direction]

            # Decide, based on direction, which coordinates to move to.
            if self.direction == Direction.right:
                self.x += 1
            elif self.direction == Direction.left:
                self.x -= 1
            elif self.direction == Direction.up:
                self.y -= 1
            elif self.direction == Direction.down:
                self.y += 1

            # If the tail should not halt, we also move each part of the tail in their respective part of the
            #   movement stack
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
                self.halt_tail = False  # Stop halting the tail for our next tick

            self.movement_stack = self.movement_stack[-len(self.tail):]  # Shave off unnecessary overhead. For memory.
            self.tail[0].new = False  # No tail part should be new after this.

            # Check Snake's head if it is by a wall and wrap him around to the other side if he is.
            if self.x <= 0:
                self.x = self.scene.width - 2
            elif self.x >= self.scene.width - 1:
                self.x = 1
            elif self.y <= 0:
                self.y = self.scene.height - 2
            elif self.y >= self.scene.height - 1:
                self.y = 1
