from RenderableObject import RenderableObject


class SnakeFood(RenderableObject):
    def __init__(self, x, y):
        super().__init__()

        self.x = x
        self.y = y

        self.sprite = "*"
