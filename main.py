import pygame

from window import GameWindow
from parameters import SCR_WIDTH, SCR_HEIGHT

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))
    pygame.display.set_caption("PACMAN")
    done = False
    clock = pygame.time.Clock()
    game = GameWindow(screen)

    while not done:
        done = game.process_events()
        game.run_logic()
        game.display_frame()
        clock.tick(30)
    pygame.quit()
