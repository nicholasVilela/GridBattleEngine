import battle_entity

class ControllableEntity(battle_entity.BattleEntity):
    def __init__(self, sprite, location, is_blue, controller, max_health):
        super().__init__(sprite, location, is_blue, max_health)
        self.controller = controller

    def update(self, grid, layer, event = None):
        self.controller.update(event)
        self.update_movement(grid)
        self.update_health()
        self.render(layer)

    def update_movement(self, grid):
        target_location = self.location.as_tuple()

        if (self.controller.move_left.pressed):
            x = target_location[0]
            y = target_location[1]

            x -= 1
            
            target_location = (x, y)

        elif (self.controller.move_right.pressed):
            x = target_location[0]
            y = target_location[1]

            x += 1
            
            target_location = (x, y)
        elif (self.controller.move_up.pressed):
            x = target_location[0]
            y = target_location[1]

            y -= 1

            target_location = (x, y)
        elif (self.controller.move_down.pressed):
            x = target_location[0]
            y = target_location[1]

            y += 1

            target_location = (x, y)

        if self.is_blue and target_location[0] < grid.columns / 2:
            self.location.change_location(grid, target_location)
        elif not self.is_blue and target_location[0] >= grid.columns / 2:
            self.location.change_location(grid, target_location)
