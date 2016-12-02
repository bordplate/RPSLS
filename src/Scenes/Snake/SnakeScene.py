from Scene import Scene
from RenderableObject import RenderableObject

from random import randint

from Scenes.Snake.SnakeObject import SnakeObject
from Scenes.Snake.Direction import Direction
from Scenes.Snake.SnakeFood import SnakeFood
from Scenes.Snake.SnakeTail import SnakeTail
from Scenes.Snake.RestartDialog import RestartDialog

import Scenes.Menu.MenuScene


class SnakeScene(Scene):
    """
    A version of the Snake game.
    """
    snake = None  # type: SnakeObject

    food = None  # type: SnakeFood

    score_label = RenderableObject()

    score = 0

    game_over = False

    restart_dialog = None  # type: RestartDialog

    def scene_will_start(self):
        """
        Sets up the game and starts it after scene setup has finished.
        :return:
        """
        self.reset()  # Does startup-configuration of the game

    def tick(self, ticks: int):
        """
        Here, we update the score label at the top of the screen.
        If the game is not over, check if the snake is on top of a snake food and add +1 to score, then add more snake
            food to the screen.
            Also, check that the snake has not collided with itself.
        :param ticks: Current engine tick count
        :return:
        """
        super().tick(ticks)

        if not self.game_over:
            if self.food:
                # Snake head and food collision check
                if self.snake.intersects_with(self.food):
                    self.add_to_score(1)

                    self.remove_object(self.food)

                    self.snake.add_tail_part()  # Snake has eaten food, make his tail longer

                    # There is a bug that seems to happen on Macs, where the width is 1 column/row more than on Linux
                    #   for some reason. So we take that in mind.
                    # Also, width/height is slightly off because of some checking in Window.py. We just make sure to
                    #   calculate for some error.
                    self.food = SnakeFood(x=randint(1, self.width-2), y=randint(1, self.height-2))

                    self.add_objects([self.food])

            # Snake head collisison checks.
            for tail_part in self.snake.tail:  # type: SnakeTail
                # Only check if the snake is intersecting with tail parts that were not JUST added.
                # New tail parts start on top of the snake head, so we'd get "false" positives.
                if self.snake.intersects_with(tail_part) and not tail_part.new:
                    self.stop_game()

    def add_to_score(self, addition: int):
        """
        Adds a specified number to the current score.
        :param addition: How many points to add to the score.
        :return: None
        """
        self.score += 1
        self.score_label.sprite = "Score: " + str(self.score)

    def stop_game(self):
        """
        Stops the game and prompts the user to restart or go back to menu.
        :return: None
        """
        self.game_over = True

        # Create restart dialog and center it
        self.restart_dialog = RestartDialog(score=self.score)
        self.restart_dialog.y = int(self.height / 2) - int(self.restart_dialog.height / 2)
        self.restart_dialog.x = int(self.width / 2) - int(self.restart_dialog.width / 2)

        self.add_objects([self.restart_dialog])

    def reset(self):
        """
        Resets all variables to their initial values.
        :return: None
        """
        self.objects = []  # Remove all objects currently on screen.
        self.game_over = False
        self.score = 0
        self.snake = SnakeObject()

        self.add_objects([self.snake])
        self.snake.add_tail_part()

        # Add food to random spot on the screen
        self.food = SnakeFood(x=randint(1, self.width-2), y=randint(1, self.height-2))

        self.score_label.sprite = "Score: " + str(self.score)

        self.add_objects([self.food, self.score_label])

    def key_pressed(self, key: str):
        """
        If the game is not over, it guides Snake in the directions specified.
            Note that in this version of Snake, Snake can go backwards and eat himself.
        If the game is over, the keys
        :param key: The key the user pressed.
        :return: None
        """
        if not self.game_over:  # Control Snake
            if key == "KEY_UP":
                self.snake.set_direction(Direction.up)
            elif key == "KEY_DOWN":
                self.snake.set_direction(Direction.down)
            elif key == "KEY_RIGHT":
                self.snake.set_direction(Direction.right)
            elif key == "KEY_LEFT":
                self.snake.set_direction(Direction.left)
        else:  # Control the restart dialog
            if key == "KEY_LEFT" or key == "KEY_RIGHT":
                self.restart_dialog.next_selection()
            elif key == "\n" or key == " ":
                if self.restart_dialog.selection == "Yes":
                    self.reset()
                else:
                    self.change_scene(Scenes.Menu.MenuScene.MenuScene())

        if key == "q":  # Exit the game at any time.
            self.change_scene(Scenes.Menu.MenuScene.MenuScene())
