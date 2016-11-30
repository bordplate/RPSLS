from Scene import Scene

from random import randint

from Scenes.Snake.SnakeObject import SnakeObject
from Scenes.Snake.Direction import Direction
from Scenes.Snake.SnakeFood import SnakeFood


class SnakeScene(Scene):
    snake = SnakeObject()

    food = None

    def scene_will_start(self):
        self.add_objects([self.snake])
        self.add_objects(self.snake.tail)

        self.food = SnakeFood(x=randint(0, 30), y=randint(0, 40))

        self.add_objects([self.food])

    def tick(self, ticks):
        super().tick(ticks)

        if self.food:
            if self.snake.intersects_with(self.food):
                self.remove_object(self.food)

                self.snake.add_tail_part()

                self.food = SnakeFood(x=randint(0, 30), y=randint(0, 30))

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
