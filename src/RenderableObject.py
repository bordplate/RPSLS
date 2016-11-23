from abc import ABCMeta, abstractmethod, abstractproperty, abstractclassmethod


class RenderableObject(metaclass=ABCMeta):
    @abstractproperty
    def x(self) -> int:
        """
        Holds the current x-position, on screen, for the object.
        :return: None
        """
        pass

    @abstractproperty
    def y(self) -> int:
        """
        Holds the current y-position, on screen, for the object.
        :return: None
        """
        pass

    @abstractproperty
    def sprite(self) -> str:
        """
        Holds the sprite (ASCII sprites) for the object.
        :return:
        """
        pass

    @abstractproperty
    def sprite_index(self) -> int:
        return 0

    @abstractproperty
    def sprite_frames(self) -> []:
        return []

    scene = None  # Scene containing the object.

    def __init__(self):
        self.sprite = ""
        self.sprite_index = 0
        self.sprite_frames = []

    def next_sprite_frame(self):
        self.sprite_index += 1

        if self.sprite_index >= len(self.sprite_frames):
            self.sprite_index = 0

        if len(self.sprite_frames) > 0:
            self.sprite = self.sprite_frames[self.sprite_index]

    def tick(self, ticks):
        pass

    def load_sprite(self, filename):
        file_contents = open(filename, 'r').read()
        frames = file_contents.split("\n-\n")

        self.sprite = frames[0]
        self.sprite_frames = frames
