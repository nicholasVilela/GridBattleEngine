import pygame, sys, constants, state
from game import Game

pygame.init()

def start():
    clock = pygame.time.Clock()
    game = Game(state.screen, True)

    def quit_game():
        pygame.quit()
        sys.exit()

    while game.running:
        game.layers['background'].fill(constants.SCREEN_FILL)
        game.layers['foreground'].fill(constants.BLACK)

        game.update()

        # # white dot at center of screen
        # tmp = pygame.image.load('../../CaveStory/Scripts/player.png')
        # game.layers['background'].blit(tmp, (game.layers['background'].get_width() / 2, game.layers['background'].get_height() / 2))

        # game.layers['background'].blit(tmp, (215, game.layers['background'].get_height() / 2))

        state.screen.blit(game.layers['background'], (0, 0))
        state.screen.blit(game.layers['midground'], (0, 0))
        state.screen.blit(game.layers['foreground'], (0, 0))


        pygame.display.update()
        clock.tick(constants.FRAMERATE)

    quit_game()

start()