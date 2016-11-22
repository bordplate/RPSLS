from RenderableObject import *


class MenuObject(RenderableObject):
    x = 0
    y = 0
    sprite = ""
    sprite_index = 0
    sprite_frames = []

    selected = False  # If this is the selected menu item

    def __init__(self):
        super().__init__()

        self.x = 3
        self.y = 2
        self.sprite = ""
        self.sprite_index = 0
        self.sprite_frames = []

    def next_sprite_frame(self):
        self.sprite_index += 1
        if self.sprite_index >= len(self.sprite_frames):
            self.sprite_index = 0

        self.sprite = self.sprite_frames[self.sprite_index]

    def tick(self, ticks):
        if self.selected:
            if ticks % 10 == 0:
                self.next_sprite_frame()
        else:
            self.sprite = self.sprite_frames[0]

        super().tick(ticks)
