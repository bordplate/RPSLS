from RenderableObject import RenderableObject

from Scenes.Snake.Direction import Direction


class SnakeTail(RenderableObject):
    """
    The tail parts for Snake.
    """
    direction = Direction.right

    new = True

    def __init__(self, direction: Direction):
        """
        Sets the direction to the specified one and sets it to new, if we init it, it must be new, right?
        :param direction: Which direction the tail part should be facing.
        """
        super().__init__()

        self.set_direction(direction)
        self.new = True

    def set_direction(self, direction: Direction):
        """
        Updates the "sprite" for the tail part appropriate to specified direction.
        :param direction: Which direction the tail part should be facing.
        :return:
        """
        self.direction = direction

        if direction == Direction.up or direction == Direction.down:
            self.sprite = "|"
        else:
            self.sprite = "-"

    def tick(self, ticks: int):
        """
        Wrap around the tail part if it is by a wall.
        :param ticks: Current engine tick count
        :return: None
        """
        super().tick(ticks)

        # If the game is over, we don't really need to do anything else.
        if self.scene.game_over:
            return

        # Wall checking and wrapping around code.
        if self.x <= 0:
            self.x = self.scene.width - 2
        elif self.x >= self.scene.width - 1:
            self.x = 1
        elif self.y <= 0:
            self.y = self.scene.height - 2
        elif self.y >= self.scene.height - 1:
            self.y = 1
