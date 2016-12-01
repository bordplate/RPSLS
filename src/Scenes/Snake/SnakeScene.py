from Scene import Scene
from RenderableObject import RenderableObject

from random import randint

from Scenes.Snake.SnakeObject import SnakeObject
from Scenes.Snake.Direction import Direction
from Scenes.Snake.SnakeFood import SnakeFood
from Scenes.Snake.SnakeTail import SnakeTail
from Scenes.Snake.RestartDialog import RestartDialog  # Re-use existing dialog code

import Scenes.Menu.MenuScene


class SnakeScene(Scene):
    snake = None  # type: SnakeObject

    food = None

    score_label = RenderableObject()

    score = 0

    game_over = False

    restart_dialog = None  # type: RestartDialog

    def scene_will_start(self):
        self.reset()  # Does startup-configuration of the game

    def tick(self, ticks):
        super().tick(ticks)

        self.score_label.sprite = "Score: " + str(self.score)

        if not self.game_over:
            if self.food:
                if self.snake.intersects_with(self.food):
                    self.score += 1

                    self.remove_object(self.food)

                    self.snake.add_tail_part()

                    self.food = SnakeFood(x=randint(1, self.width-2), y=randint(1, self.height-2))

                    self.add_objects([self.food])

            for tail_part in self.snake.tail:  # type: SnakeTail
                if self.snake.intersects_with(tail_part) and not tail_part.new:
                    self.stop_game()

    def stop_game(self):
        self.game_over = True
        self.restart_dialog = RestartDialog(score=self.score)
        self.restart_dialog.y = int(self.height / 2) - int(self.restart_dialog.height / 2)
        self.restart_dialog.x = int(self.width / 2) - int(self.restart_dialog.width / 2)

        self.add_objects([self.restart_dialog])

    def reset(self):
        if self.snake:
            del self.snake

        self.objects = []  # Remove all objects currently on screen.
        self.game_over = False
        self.score = 0
        self.snake = SnakeObject()

        self.add_objects([self.snake])
        self.snake.add_tail_part()

        self.food = SnakeFood(x=randint(1, self.width-1), y=randint(1, self.height-1))

        self.score_label.sprite = "Score: " + str(self.score)

        self.add_objects([self.food, self.score_label])

    def key_pressed(self, key: str):
        """

        :param key:
        :return:
        """
        if not self.game_over:
            if key == "KEY_UP":
                self.snake.set_direction(Direction.up)
            elif key == "KEY_DOWN":
                self.snake.set_direction(Direction.down)
            elif key == "KEY_RIGHT":
                self.snake.set_direction(Direction.right)
            elif key == "KEY_LEFT":
                self.snake.set_direction(Direction.left)
        else:
            if key == "KEY_LEFT" or key == "KEY_RIGHT":
                self.restart_dialog.next_selection()
            elif key == "\n" or key == " ":
                if self.restart_dialog.selection == "Yes":
                    self.reset()
                else:
                    self.change_scene(Scenes.Menu.MenuScene.MenuScene())

        if key == "q":
            self.change_scene(Scenes.Menu.MenuScene.MenuScene())

    def render(self):
        pass
