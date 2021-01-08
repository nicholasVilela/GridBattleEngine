import numpy, constants, create, panel_entity, helper, state, pygame

class Grid:
    def __init__(self, columns, rows, scale, space_between_tiles):
        self.columns = columns
        self.rows = rows
        self.scale = scale
        self.space_between_tiles = space_between_tiles

        self.panels = self.construct_grid()

    def update(self, layers):
        for y in range(0, self.rows):
            for x in range(0, self.columns):
                panel = self.panels[y][x]
                panel.update(layers['midground'])

    def get_tile_space(self, length):
        return length * self.scale + self.space_between_tiles

    def get_panel_path(self, is_blue):
        return constants.Tiles.NORMAL['blue_3'] if is_blue else constants.Tiles.NORMAL['red_3']

    def to_center(self, panel_grid, starting_raw_x, starting_raw_y, x_center, y_center):
        center_of_grid_x = (starting_raw_x + self.get_tile_space(constants.Tiles.WIDTH) * self.columns / 2) - self.space_between_tiles
        distance_x = x_center - center_of_grid_x

        center_of_grid_y = (starting_raw_y + self.get_tile_space(constants.Tiles.HEIGHT) * self.rows / 2) - self.space_between_tiles
        distance_y = y_center - center_of_grid_y

        for row in panel_grid:
            for panel in row:
                panel.location.raw_x += distance_x
                panel.location.raw_y += distance_y

    def construct_grid(self):
        panel_grid = numpy.empty((self.rows, self.columns), panel_entity.PanelEntity)

        x_center = state.screen.get_width() / 2
        y_center = state.screen.get_height() / 2

        starting_raw_x = x_center - self.get_tile_space(constants.Tiles.WIDTH)  * self.columns
        starting_raw_y = y_center - self.get_tile_space(constants.Tiles.HEIGHT) * self.rows

        raw_x = starting_raw_x
        raw_y = starting_raw_y

        for y in range(0, self.rows):
            for x in range(0, self.columns):
                is_blue = x < (self.columns / 2)
                
                location = create.location(x, y, raw_x, raw_y, 0, 0)

                sprite_path = self.get_panel_path(is_blue)
                sprite = create.sprite(sprite_path, self.scale)

                panel = create.panel_entity(sprite, location, is_blue)

                panel_grid[y][x] = panel

                raw_x += self.get_tile_space(constants.Tiles.WIDTH)
            
            raw_x = starting_raw_x
            raw_y += self.get_tile_space(constants.Tiles.HEIGHT)

        self.to_center(panel_grid, starting_raw_x, starting_raw_y, x_center, y_center)

        return panel_grid