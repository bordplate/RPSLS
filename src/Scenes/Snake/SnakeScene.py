from Scene import Scene
from RenderableObject import RenderableObject

from random import randint

from Scenes.Snake.SnakeObject import SnakeObject
from Scenes.Snake.Direction import Direction
from Scenes.Snake.SnakeFood import SnakeFood
from Scenes.Snake.SnakeTail import SnakeTail


class SnakeScene(Scene):
    snake = SnakeObject()

    food = None

    score_label = RenderableObject()

    score = 0

    def scene_will_start(self):
        self.add_objects([self.snake])
        self.snake.add_tail_part()

        self.food = SnakeFood(x=randint(1, self.width-1), y=randint(1, self.height-1))

        self.score_label.sprite = "Score: " + str(self.score)

        self.add_objects([self.food, self.score_label])

    def tick(self, ticks):
        super().tick(ticks)

        self.score_label.sprite = "Score: " + str(self.score)

        if self.food:
            if self.snake.intersects_with(self.food):
                self.score += 1

                self.remove_object(self.food)

                self.snake.add_tail_part()

                self.food = SnakeFood(x=randint(1, self.width-2), y=randint(1, self.height-2))

                self.add_objects([self.food])

    def key_pressed(self, key: str):
        """

        :param key:
        :return:
        """
        if key == "KEY_UP":
            self.snake.set_direction(Direction.up)
        elif key == "KEY_DOWN":
            self.snake.set_direction(Direction.down)
        elif key == "KEY_RIGHT":
            self.snake.set_direction(Direction.right)
        elif key == "KEY_LEFT":
            self.snake.set_direction(Direction.left)

    def render(self):
        pass
