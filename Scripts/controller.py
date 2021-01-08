class Controller:
    def __init__(
        self, 
        move_left, 
        move_right, 
        move_up, 
        move_down
        ):
        self.move_left = move_left
        self.move_right = move_right
        self.move_up = move_up
        self.move_down = move_down
        self.buttons = []

        self.buttons.append(self.move_left)
        self.buttons.append(self.move_right)
        self.buttons.append(self.move_up)
        self.buttons.append(self.move_down)

    def update(self, event):
        for button in self.buttons:
            button.update(event)