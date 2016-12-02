from RenderableObject import RenderableObject


class RestartDialog(RenderableObject):
    """
    A dialog that prompts the user to restart or not.
    Also shows the final score.
    """
    selection = "Yes"  # Default to "Yes, restart"

    def next_selection(self):
        """
        Selects the next item in the dialog.
        :return: None
        """
        self.next_sprite_frame()
        if self.selection == "Yes":
            self.selection = "No"
        else:
            self.selection = "Yes"

    def __init__(self, score: int):
        """
        Loads the dialog from sprite file and replaces placeholder value for score with actual score.
        :param score: Score the player got.
        """
        super().__init__()

        self.load_sprite("sprites/restart-snake.txt")

        # Replace "000" in sprites with actual score in all frames of the dialog.
        for i, sprite in enumerate(self.sprite_frames):
            self.sprite_frames[i] = sprite.replace("000", str(score).zfill(3))

        self.sprite = self.sprite_frames[0]
