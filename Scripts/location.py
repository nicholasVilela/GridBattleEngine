import helper

class Location:
    def __init__(self, x, y, raw_x, raw_y, offset_x, offset_y):
        self.x = x
        self.y = y
        self.raw_x = raw_x
        self.raw_y = raw_y
        self.offset_x = offset_x
        self.offset_y = offset_y

    def as_tuple(self):
        return (self.x, self.y)

    def as_raw_tuple(self):
        return (self.raw_x, self.raw_y)

    def change_location(self, grid, target_location):
        if helper.is_valid_location(grid, target_location):
            self.x = target_location[0] if target_location[0] != self.x else self.x
            self.y = target_location[1] if target_location[1] != self.y else self.y

            self.change_raw_location(helper.get_raw_location(grid.panels, self.as_tuple()))

    def change_raw_location(self, target_location):
        self.raw_x = target_location[0] + self.offset_x if target_location[0] != self.raw_x else (self.raw_x + self.offset_x)
        self.raw_y = target_location[1] + self.offset_y if target_location[1] != self.raw_y else (self.raw_y + self.offset_y)
