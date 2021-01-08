from entity import Entity

class PanelEntity(Entity):
    def __init__(self, sprite, location, is_blue):
        super().__init__(sprite, location)
        self.is_blue = is_blue