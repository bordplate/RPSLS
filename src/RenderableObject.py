from abc import ABCMeta


class RenderableObject(metaclass=ABCMeta):
    x = 0
    y = 0

    sprite = ""
    sprite_frames = []
    sprite_index = 0
    sprite_style = 0

    scene = None  # Scene containing the object.

    def __init__(self):
        pass

    def next_sprite_frame(self):
        """
        Sets the sprite to the next animation frame. Wraps around if needed.
        :return: None
        """
        self.sprite_index += 1

        if self.sprite_index >= len(self.sprite_frames):
            self.sprite_index = 0

        if len(self.sprite_frames) > 0:
            self.sprite = self.sprite_frames[self.sprite_index]

    def tick(self, ticks):
        pass

    def load_sprite(self, filename):
        """
        Loads a sprite into this object.
        :param filename: Path to the sprite
        :return: None
        """
        file_contents = open(filename, 'r').read()
        frames = file_contents.split("\n-\n")

        self.sprite = frames[0]
        self.sprite_frames = frames
