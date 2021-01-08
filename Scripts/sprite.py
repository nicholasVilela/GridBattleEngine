import pygame

class Sprite:
    def __init__(self, path, scale):
        self.path = path
        self.scale = scale

    def load_sprite(self):
        return pygame.image.load(self.path)

    def as_scale(self):
        image = self.load_sprite()
        width = image.get_width()
        height = image.get_height()
        return pygame.transform.scale(image, (width * self.scale, height * self.scale))