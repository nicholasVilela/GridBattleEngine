import pygame

class Button:
    def __init__(self, name, key):
        self.name = name
        self.key = key
        self.pressed = False
        self.released = False
        self.holding = False
        
    def update(self, event):
        if event == None:
            self.pressed = False
            self.released = False
            self.holding = False
        else:
            self.pressed = event.key == self.key if event.type == pygame.KEYDOWN else False
            self.released = event.key == self.key if event.type == pygame.KEYUP else False
            self.holding = pygame.key.get_pressed()[self.key]