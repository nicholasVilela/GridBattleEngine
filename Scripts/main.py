import pygame, sys, constants, numpy

pygame.init()
screen = pygame.display.set_mode(constants.SCREEN_SIZE)
background = pygame.Surface((constants.SCREEN_SIZE[0], constants.SCREEN_SIZE[1]))
panels = pygame.Surface((constants.SCREEN_SIZE[0], constants.SCREEN_SIZE[1]))
panels.set_colorkey(constants.BLACK)
foreground = pygame.Surface((constants.SCREEN_SIZE[0], constants.SCREEN_SIZE[1]))
foreground.set_colorkey(constants.BLACK)

def create_location(x, y, raw_x, raw_y, offset_x, offset_y):
    return Location(x, y, raw_x, raw_y, offset_x, offset_y)

def create_sprite(path, scale):
    return Sprite(path, scale)

def create_animated_sprite(path, frame_count, frame_rate):
    return AnimatedSprite(path, frame_count, frame_rate)

def create_entity(sprite, location):
    return Entity(sprite, location)

def create_battle_entity(sprite, location, is_blue):
    return BattleEntity(sprite, location, is_blue)

def create_controllable_entity(sprite, location, controller, is_blue):
    return ControllableEntity(sprite, location, controller, is_blue)

def create_panel(sprite, location, is_blue):
    return Panel(sprite, location, is_blue)

def create_grid(rows, columns):
    return Grid(rows, columns)


def create_controller():
        return Controller(
            Button('Left', pygame.K_LEFT),
            Button('Right', pygame.K_RIGHT),
            Button('Up', pygame.K_UP),
            Button('Down', pygame.K_DOWN))

def create_alt_controller():
        return Controller(
            Button('Left', pygame.K_a),
            Button('Right', pygame.K_d),
            Button('Up', pygame.K_w),
            Button('Down', pygame.K_s))


def get_raw_location_from_location(grid, location):
    return grid.map[location[0]][location[1]].location.as_raw_tuple()

def get_panel_from_location(grid, location):
    return grid.map[location[0]][location[1]].location.as_tuple()

def is_valid_location(grid, location):
    return (location[0] >= 0 and location[0] < grid.rows) and (location[1] >= 0 and location[1] < grid.columns)


def get_sprite_as_scale(sprite):
    return pygame.transform.scale(sprite.get_sprite(), sprite.scale)

def get_resolution_by_scale(width, height, scale):
    return (width * scale, height * scale)


class Controller:
    def __init__(
        self, 
        move_left, 
        move_right, 
        move_up, 
        move_down
        ):
        self.move_left = move_left
        self.move_right = move_right
        self.move_up = move_up
        self.move_down = move_down
        self.buttons = []

        self.buttons.append(self.move_left)
        self.buttons.append(self.move_right)
        self.buttons.append(self.move_up)
        self.buttons.append(self.move_down)

    def update(self, event):
        for button in self.buttons:
            button.update(event)

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


class Location:
    def __init__(self, x, y, raw_x, raw_y, offset_x, offset_y):
        self.x = x
        self.y = y
        self.raw_x = raw_x + offset_x
        self.raw_y = raw_y + offset_y
        self.offset_x = offset_x
        self.offset_y = offset_y

    def change_location(self, grid, target_location):
        if is_valid_location(grid, target_location):
            self.x = target_location[0] if target_location[0] != self.x else self.x
            self.y = target_location[1] if target_location[1] != self.y else self.y

            self.change_raw_location(get_raw_location_from_location(grid, self.as_tuple()))

    def change_raw_location(self, target_location):
        self.raw_x = target_location[0] + self.offset_x if target_location[0] != self.raw_x else (self.raw_x + self.offset_x)
        self.raw_y = target_location[1] + self.offset_y if target_location[1] != self.raw_y else (self.raw_y + self.offset_y)

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

    def update(self, grid, event = None):
        self.render()

    def render(self):
        image = self.sprite.get_sprite()
        background.blit(image, self.location.as_raw_tuple())

class BattleEntity(Entity):
    def __init__(self, sprite, location, is_blue):
        super().__init__(sprite, location)
        self.is_blue = is_blue

    def render(self):
        image = get_sprite_as_scale(self.sprite)
        foreground.blit(image, self.location.as_raw_tuple())

class ControllableEntity(BattleEntity):
    def __init__(self, sprite, location, controller, is_blue):
        super().__init__(sprite, location, is_blue)
        self.controller = controller

    def update(self, grid, event = None):
        self.controller.update(event)
        self.update_movement(grid)
        self.render()

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

        if self.is_blue and target_location[0] < grid.rows / 2:
            self.location.change_location(grid, target_location)
        elif not self.is_blue and target_location[0] >= grid.rows / 2:
            self.location.change_location(grid, target_location)

        
    
class Panel(Entity):
    def __init__(self, sprite, location, is_blue):
        super().__init__(sprite, location)
        self.is_blue = is_blue

    def update(self):
        self.render()

    def render(self):
        image = get_sprite_as_scale(self.sprite)
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
                panel.update()

    def construct_grid(self):
        map = numpy.empty((self.rows, self.columns), Panel)

        x_center = background.get_width() / 2
        y_center = background.get_height() / 2

        x_original_location = x_center - ((constants.TILES.WIDTH * self.scale + self.scale) * self.columns) + 2

        x_location = x_original_location
        y_location = y_center - ((constants.TILES.HEIGHT * self.rows) / 4 * self.scale + 4)

        for column in range(0, self.columns):
            for row in range(0, self.rows):
                is_blue = row < (self.rows / 2)
                sprite = self.load_panel(is_blue)
                location = create_location(row, column, x_location, y_location, 0, 0)

                panel = create_panel(sprite, location, is_blue)
                map[row][column] = panel

                x_location += constants.TILES.WIDTH * self.scale + self.scale

            x_location = x_original_location
            y_location += constants.TILES.HEIGHT * self.scale + self.scale

        return map

    def load_panel(self, is_blue):
        sprite_path = constants.TILES.NORMAL['blue'] if is_blue else constants.TILES.NORMAL['red']
        # sprite_path = constants.TILES.NORMAL['blue_2'] if is_blue else constants.TILES.NORMAL['red_2']
        scale = get_resolution_by_scale(constants.TILES.WIDTH, constants.TILES.HEIGHT, self.scale)

        return create_sprite(sprite_path, scale)


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

        self.player = create_controllable_entity(
            create_sprite(constants.PLAYER.SPRITES['idle'], get_resolution_by_scale(constants.PLAYER.WIDTH, constants.PLAYER.HEIGHT, 2)),
            create_location(1, 1, get_raw_location_from_location(self.grid, (1, 1))[0], get_raw_location_from_location(self.grid, (1, 1))[1], constants.PLAYER.OFFSET_X, constants.PLAYER.OFFSET_Y),
            create_controller(),
            True
        )

        self.enemy = create_controllable_entity(
            create_sprite(constants.PLAYER.SPRITES['idle'], get_resolution_by_scale(constants.PLAYER.WIDTH, constants.PLAYER.HEIGHT, 2)),
            create_location(6, 1, get_raw_location_from_location(self.grid, (6, 1))[0], get_raw_location_from_location(self.grid, (6, 1))[1], constants.PLAYER.OFFSET_X, constants.PLAYER.OFFSET_Y),
            create_alt_controller(),
            False
        )

        self.entities.append(self.player) 
        self.entities.append(self.enemy)

    def update(self):
        self.update_events()
        self.grid.update()

    def update_entities(self, event = None):
        for entity in self.entities:
            entity.update(self.grid, event)

    def update_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            else:
                self.update_entities(event)

        self.update_entities()


def start():
    clock = pygame.time.Clock()
    game = Game(screen)

    def quit_game():
        pygame.quit()
        sys.exit()


    while game.running:
        background.fill(constants.SCREEN_FILL)
        foreground.fill(constants.BLACK)
        game.update()

        # white dot at center of screen
        # tmp = pygame.image.load('../../CaveStory/Scripts/player.png')
        # background.blit(tmp, (background.get_width() / 2, background.get_height() / 2))

        screen.blit(background, (0, 0))
        screen.blit(panels, (0, 0))
        screen.blit(foreground, (0, 0))


        pygame.display.update()
        clock.tick(constants.FRAMERATE)

    quit_game()

start()