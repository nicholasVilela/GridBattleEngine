import pygame, create, constants, helper, random, state

class Game:
    def __init__(self, screen, is_single_player):
        self.screen = screen
        self.is_single_player = is_single_player
        self.running = True

        # self.grid = create.grid(1, 2, 4, 2)
        # self.grid = create.grid(2, 4, 2, 2)
        # self.grid = create.grid(3, 6, 2, 2)
        self.grid = create.grid(8, 4, 3, 2)
        # self.grid = create.grid(5, 10, 1, 2)

        self.create_layers()
        self.create_battle_entities()
        

    def update(self):
        self.update_events()
        self.grid.update(self.layers)

    def update_entities(self, event = None):
        for entity in state.entities:
            entity.update(self.grid, self.layers['foreground'], event)

    def update_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                self.running = False
            else:
                self.update_entities(event)

        self.update_entities()

    def create_battle_entities(self):
        self.create_controllable_entities()

        enemies = [
            {
                'sprite': create.sprite(constants.Enemy.SPRITES['ghost'], 2),
                'location': create.location(5, 1, helper.get_raw_location(self.grid.panels, (5, 1))[0], helper.get_raw_location(self.grid.panels, (5, 1))[1], 23, -25),
                'max_health': 00
            },
            {
                'sprite': create.sprite(constants.Enemy.SPRITES['ghost'], 2),
                'location': create.location(7, 3, helper.get_raw_location(self.grid.panels, (7, 3))[0], helper.get_raw_location(self.grid.panels, (7, 3))[1], 23, -25),
                'max_health': 20
            }]
        self.create_enemies(enemies)

    def create_enemies(self, enemies):
        for enemy in enemies:
            enemy_entity = create.battle_entity(enemy['sprite'], enemy['location'], False, enemy['max_health'])
            state.entities.append(enemy_entity)

    def create_controllable_entities(self):
        if self.is_single_player:
            sprite = create.sprite(constants.Player.SPRITES['idle'], 2)
            raw_location = helper.get_raw_location(self.grid.panels, (1, 1))
            # location = create.location(4, 1, raw_location[0], raw_location[1], 12 / sprite.scale, -12 / sprite.scale)
            location = create.location(1, 1, raw_location[0], raw_location[1], -7, -30)
            controller = create.controller()
            player = create.controllable_entity(sprite, location, True, controller, 600)

            state.entities.append(player)
        else:
            pass

    def create_layers(self):
        background = pygame.Surface((constants.SCREEN_SIZE[0], constants.SCREEN_SIZE[1]))

        midground = pygame.Surface((constants.SCREEN_SIZE[0], constants.SCREEN_SIZE[1]))
        midground.set_colorkey(constants.BLACK)

        foreground = pygame.Surface((constants.SCREEN_SIZE[0], constants.SCREEN_SIZE[1]))
        foreground.set_colorkey(constants.BLACK)

        self.layers = {
            'background': background,
            'midground' : midground,
            'foreground': foreground
        }