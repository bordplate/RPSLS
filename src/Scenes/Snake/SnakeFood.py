from RenderableObject import RenderableObject


class SnakeFood(RenderableObject):
    """
    The food Snake eats.
    """
    def __init__(self, x, y):
        """
        Sets position and sprite.
        :param x: x coordinate for object.
        :param y: y coordinate for object.
        """
        super().__init__()

        self.set_position(x, y)

        self.sprite = "*"
