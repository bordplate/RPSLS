from abc import ABCMeta

import Scene  # Needed for proper type annotations.

class RenderableObject(metaclass=ABCMeta):
    """
    An object that the engine will recognize as renderable and draw on screen.
    """
    x = 0
    y = 0

    width = 0
    height = 0

    sprite = ""  # Holds the sprite that will be drawn on screen.
    sprite_frames = []  # Holds animation frames
    sprite_index = 0  # Holds the current index for animation frames.

    # Scene currently holding this object.
    scene = None   # type: Scene.Scene

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

    def tick(self, ticks: int):
        """
        Not doing anything in this case.
        Can be used in sub-classes if we want to get a call for every tick.
        :param ticks: Current engine tick count
        :return: None
        """
        pass

    def flip_sprite(self):
        """
        Flips the sprite around (e.g. mirrors it)
        Tries to not flip text if it detects it in the sprite.
        :return: None
        """
        flipped_sprite = ""  # Temp to hold flipped sprite before assigning it to self.sprite.

        for string in self.sprite.split("\n"):
            # If there are at least 2 alpha characters, assume that line is just text and don't flip that line
            if sum(c.isalpha() for c in string) >= 2:
                flipped_sprite += string + "\n"
                continue

            # When mirroring, spaces will get lost on some lines, so we restore them based on width of the sprite.
            for i in range(len(string), self.width):
                flipped_sprite += " "

            flipped_sprite += string[::-1] + "\n"  # Flips order of characters in the string

        flipped_sprite = flipped_sprite.translate(str.maketrans("()/\\", ")(\\/"))  # Flip directional characters

        self.sprite = flipped_sprite

    def set_position(self, x: int, y: int):
        """
        Function that is more practical than explicitly setting x and y.
        :param x: x-position for object
        :param y: y-position for object
        :return: None
        """
        self.x = x
        self.y = y

    def intersects_with(self, other_object) -> bool:
        """
        Checks if current object intersects with another object (Collision detection)
        :param other_object: The object to check. Must be of RenderableObject
        :return: Whether or not the objects intersect
        """
        if other_object.x < self.x < other_object.x + other_object.width:
            # Current x and width within object's position
            if other_object.y <= self.y <= other_object.y + other_object.width:
                # Current y and height also within object's position
                return True
            elif self.y <= other_object.y <= self.y + self.width:
                return True
        elif self.x <= other_object.x <= self.x + self.width:
            # Also check the other object, to see if they are within this object's position.
            if self.y <= other_object.y <= self.y + self.width:
                return True
            elif self.y <= other_object.y <= self.y + self.width:
                return True

        # If none of the above, assume we're not intersecting.
        return False

    def load_sprite(self, filename: str):
        """
        Loads a sprite into this object.
        Assigns self.width and height to appropriate values.
        Also loads all animation frames in self.sprite_frames
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
