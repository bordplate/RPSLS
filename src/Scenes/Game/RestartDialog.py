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

    def __init__(self, winner: int):
        super().__init__()

        self.load_sprite("sprites/restart.txt")

        if winner < 3:
            # Replace "Player N" in sprites with actual winning player.
            for i, sprite in enumerate(self.sprite_frames):
                self.sprite_frames[i] = sprite.replace("Player N", "Player " + str(winner))
        else:
            # Replace "Player N" in sprites with tie-message.
            for i, sprite in enumerate(self.sprite_frames):
                self.sprite_frames[i] = sprite.replace("Player N wins!", "That is a tie!")

        self.sprite = self.sprite_frames[0]

    pass
