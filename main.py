import pygame

from game_window import GameWindow
from parametrs import SCREEN_WIDTH, SCREEN_HEIGHT

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
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
