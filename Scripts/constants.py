import pygame

# SCREEN_SIZE = (1200, 960)
SCREEN_SIZE = (600, 480)
# SCREEN_SIZE = (1280, 1024)

SCREEN_FILL = (134,97,97)

FRAMERATE = 60

class PLAYER:
    SPRITES = {
        'idle': '../Sprites/Player/idle_1.png'
    }

class TILES:
    # RED = {
    #     'normal': '../Sprites/Map/tile_red_normal.png',
    #     'normal_2': '../Sprites/Map/tile_red_normal_2.png', 
    # }
    # BLUE = {
    #     'normal': '../Sprites/Map/tile_blue_normal.png',
    #     'normal_2': '../Sprites/Map/tile_blue_normal_2.png', 
    # }

    # NORMAL = {
    #     'red': '../Sprites/Map/tile_red_normal.png',
    #     'blue': '../Sprites/Map/tile_blue_normal.png'
    # }
    # NORMAL_2 = {
    #     'red': '../Sprites/Map/tile_red_normal_2.png',
    #     'blue': '../Sprites/Map/tile_blue_normal_2.png'
    # }
    NORMAL = {
        'red': '../Sprites/Map/tile_normal_red.png',
        'blue': '../Sprites/Map/tile_normal_blue.png',
        'red_2': '../Sprites/Map/tile_normal_red_2.png',
        'blue_2': '../Sprites/Map/tile_normal_blue_2.png'
    }


    WIDTH = pygame.image.load(NORMAL['red']).get_width()
    HEIGHT = pygame.image.load(NORMAL['red']).get_height()
    # WIDTH = pygame.image.load(NORMAL['red_2']).get_width()
    # HEIGHT = pygame.image.load(NORMAL['red_2']).get_height()
