import entity, state

class BattleEntity(entity.Entity):
    def __init__(self, sprite, location, is_blue, max_health):
        super().__init__(sprite, location)
        self.is_blue = is_blue
        self.max_health = max_health
        self.health = max_health
        self.alive = True

    def update(self, grid, layer, event = None):
        self.update_health()
        self.render(layer)

    def kill(self):
        self.health = 0
        self.alive = False
        state.entities = list(filter(lambda x: x.alive, state.entities))

    def update_health(self):
        if self.health <= 0 and self.alive:
            self.kill()
