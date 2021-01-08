import state, constants

def get_raw_location(panel_grid, location):
    return panel_grid[location[1]][location[0]].location.as_raw_tuple()

def get_panel(grid, location):
    return grid.panels_grid[location[1]][location[0]]

def is_valid_location(grid, location):
    return (location[0] >= 0 and location[0] < grid.columns) and (location[1] >= 0 and location[1] < grid.rows)

def is_alive(entity):
    return entity.is_alive