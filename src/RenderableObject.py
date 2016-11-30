from abc import ABCMeta


class RenderableObject(metaclass=ABCMeta):
    x = 0
    y = 0

    width = 0
    height = 0

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

    def flip_sprite(self):
        """
        Flips the sprite around (e.g. mirrors it)
        :return: None
        """

        flipped_sprite = ""
        for string in self.sprite.split("\n"):
            # If there are at least 2 alpha characters, assume that line is just text and don't flip that line
            if sum(c.isalpha() for c in string) >= 2:
                flipped_sprite += string + "\n"
                continue

            for i in range(len(string), self.width):
                flipped_sprite += " "  # Add missing spaces to current line, if any.

            flipped_sprite += string[::-1] + "\n"

        flipped_sprite = flipped_sprite.translate(str.maketrans("()/\\", ")(\\/"))  # Flip directional characters

        self.sprite = flipped_sprite

    def set_position(self, x: int, y: int):
        """
        Function that is more practical than explicitly setting x and y.
        :param x: x-position for object
        :param y: y-position for object
        :return:
        """
        self.x = x
        self.y = y

    def intersects_with(self, other_object) -> bool:
        """
        Checks if current object intersects with another object
        :param other_object: The object to check
        :return: Whether or not the objects intersect
        """
        if other_object.x < self.x < other_object.x + other_object.width:
            if other_object.y <= self.y <= other_object.y + other_object.width:
                return True
            elif self.y <= other_object.y <= self.y + self.width:
                return True
        elif self.x <= other_object.x <= self.x + self.width:
            if self.y <= other_object.y <= self.y + self.width:
                return True
            elif self.y <= other_object.y <= self.y + self.width:
                return True

        return False

    def load_sprite(self, filename: str):
        """
        Loads a sprite into this object.
        :param filename: Path to the sprite
        :return: None
        """
        file_contents = open(filename, 'r').read()
        frames = file_contents.split("\n-\n")

        self.sprite = frames[0]
        self.sprite_frames = frames

        # Add 1 to height for every line break and assign width to the longest line in the sprite
        for line in self.sprite.split("\n"):
            self.height += 1
            if len(line) > self.width:
                self.width = len(line)
