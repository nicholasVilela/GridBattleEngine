import pygame, sys, constants, numpy

pygame.init()
screen = pygame.display.set_mode(constants.SCREEN_SIZE)
display = pygame.Surface((constants.SCREEN_SIZE[0], constants.SCREEN_SIZE[1]))
panels = pygame.Surface((constants.SCREEN_SIZE[0], constants.SCREEN_SIZE[1]))

def create_location(x, y, raw_x, raw_y):
    return Location(x, y, raw_x, raw_y)

def create_sprite(path, scale):
    return Sprite(path, scale)

def create_animated_sprite(path, frame_count, frame_rate):
    return AnimatedSprite(path, frame_count, frame_rate)

def create_entity(sprite, location):
    return Entity(sprite, location)

def create_battle_entity(sprite, location):
    return BattleEntity(sprite, location)

def create_panel(sprite, location, is_blue):
    return Panel(sprite, location, is_blue)

def create_grid(rows, columns):
    return Grid(rows, columns)


def get_raw_location_from_location(grid, x, y):
    return grid.map[x][y].location.as_raw_tuple()

def get_sprite_as_scale(sprite, scale):
    return pygame.transform.scale(sprite.get_sprite(), scale)


class Location:
    def __init__(self, x, y, raw_x, raw_y):
        self.x = x
        self.y = y
        self.raw_x = raw_x
        self.raw_y = raw_y

    def change_location(self, target_x, target_y):
        self.x = target_x if target_x != self.x else self.x
        self.y = target_y if target_y != self.y else self.y

    def change_raw_location(self, target_x, target_y):
        self.raw_x = target_x if target_x != self.raw_x else self.raw_x
        self.raw_y = target_y if target_y != self.raw_y else self.raw_y

    def as_tuple(self):
        return (self.x, self.y)

    def as_raw_tuple(self):
        return (self.raw_x, self.raw_y)


class Sprite:
    def __init__(self, path, scale):
        self.path = path
        self.scale = scale

    def get_sprite(self):
        return pygame.image.load(self.path)

class AnimatedSprite(Sprite):
    def __init__(self, path, frame_count, frame_rate):
        super().__init__(path)
        self.frame_count = frame_count
        self.frame_rate = frame_rate
        self.frame = 1


class Entity:
    def __init__(self, sprite, location):
        self.sprite = sprite
        self.location = location
        self.moving = False

    def update(self):
        self.render()

    def render(self):
        # image = self.sprite.scale_to_display(self.sprite.get_sprite())
        image = self.sprite.get_sprite()
        # image = self.sprite.get_sprite_as_scale((int(constants.SCREEN_SIZE[0] / 2), int(constants.SCREEN_SIZE[1] / 2)))
        display.blit(image, self.location.as_raw_tuple())

class BattleEntity(Entity):
    def __init__(self, sprite, location):
        super().__init__(sprite, location)

    
class Panel(Entity):
    def __init__(self, sprite, location, is_blue):
        super().__init__(sprite, location)
        self.is_blue = is_blue

    def update(self, resolution):
        self.render(resolution)

    def render(self, resolution):
        image = get_sprite_as_scale(self.sprite, resolution)
        panels.blit(image, self.location.as_raw_tuple())
    
class Grid:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.scale = 3
        self.map = self.construct_grid()

    def update(self):
        for row in range(0, self.rows):
            for column in range(0, self.columns):
                panel = self.map[row][column]
                resolution = (constants.TILES.WIDTH * self.scale, constants.TILES.HEIGHT * self.scale)
                panel.update(resolution)

    def construct_grid(self):
        map = numpy.empty((self.rows, self.columns), Panel)

        x_center = display.get_width() / 2
        y_center = display.get_height() / 2

        # x_center = display.get_width() / 2 - constants.TILES.WIDTH / 2
        # y_center = display.get_height() / 2 - constants.TILES.HEIGHT / 2

        # x_original_location = x_center - ((constants.TILES.WIDTH * (self.columns * self.scale)))
        x_original_location = x_center - ((constants.TILES.WIDTH * self.scale + self.scale) * self.columns) + 2
        x_location = x_original_location
        y_location = y_center - ((constants.TILES.HEIGHT * self.rows) / 4 * self.scale + 4)

        for column in range(0, self.columns):
            for row in range(0, self.rows):
                is_blue = row < (self.rows / 2)
                sprite = self.load_sprite(is_blue)
                location = create_location(row, column, x_location, y_location)

                panel = create_panel(sprite, location, is_blue)
                map[row][column] = panel

                x_location += constants.TILES.WIDTH * self.scale + self.scale

            x_location = x_original_location
            y_location += constants.TILES.HEIGHT * self.scale + self.scale

        return map

    def load_sprite(self, is_blue):
        sprite_path = constants.TILES.NORMAL['blue'] if is_blue else constants.TILES.NORMAL['red']
        # sprite_path = constants.TILES.NORMAL['blue_2'] if is_blue else constants.TILES.NORMAL['red_2']
        return create_sprite(sprite_path, self.scale)



class Game:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.entities = []
        # self.grid = create_grid(1, 1)
        # self.grid = create_grid(4, 2)
        # self.grid = create_grid(6, 3)
        self.grid = create_grid(8, 4)
        # self.grid = create_grid(10, 5)
        # self.grid = create_grid(12, 6)
        # self.grid = create_grid(14, 7)
        self.player = create_entity(get_sprite_as_scale(create_sprite(constants.PLAYER.SPRITES['idle'], 2), 2), create_location(1, 1, get_raw_location_from_location(self.grid, 1, 1)[0], get_raw_location_from_location(self.grid, 1, 1)[1]))
        print(self.player.location.as_raw_tuple())
        self.entities.append(self.player)

    def update(self):
        self.update_entities()
        self.update_events()
        self.grid.update()

    def update_entities(self):
        for entity in self.entities:
            entity.update()

    def update_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False


def start():
    clock = pygame.time.Clock()
    game = Game(screen)

    def quit_game():
        pygame.quit()
        sys.exit()


    while game.running:
        display.fill(constants.SCREEN_FILL)
        game.update()

        # white dot at center of screen
        # tmp = pygame.image.load('../../CaveStory/Scripts/player.png')
        # display.blit(tmp, (display.get_width() / 2, display.get_height() / 2))

        # panel_surf = pygame.transform.scale(panels, constants.SCREEN_SIZE)
        # display.blit(panels, (0, 0))

        display_surf = pygame.transform.scale(display, constants.SCREEN_SIZE)
        screen.blit(display_surf, (0, 0))


        pygame.display.update()
        clock.tick(constants.FRAMERATE)

    quit_game()

start()