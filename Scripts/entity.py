import helper

class Entity:
    def __init__(self, sprite, location):
        self.sprite = sprite
        self.location = location

    def update(self, layer):
        self.render(layer)

    def render(self, layer):
        image = self.sprite.as_scale()
        target_location = (self.location.raw_x + self.location.offset_x, self.location.raw_y + self.location.offset_y)
        layer.blit(image, target_location)