from RenderableObject import RenderableObject


class RestartDialog(RenderableObject):
    selection = "Yes"

    def next_selection(self):
        """
        Selects the next item in the dialog.
        :return:
        """
        self.next_sprite_frame()
        if self.selection == "Yes":
            self.selection = "No"
        else:
            self.selection = "Yes"

    def __init__(self, score: int):
        super().__init__()

        self.load_sprite("sprites/restart-snake.txt")

        # Replace "000" in sprites with actual score.
        for i, sprite in enumerate(self.sprite_frames):
            self.sprite_frames[i] = sprite.replace("000", str(score).zfill(3))

        self.sprite = self.sprite_frames[0]
