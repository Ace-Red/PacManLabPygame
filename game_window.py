import argparse
import sys

import pygame.mixer

from game import Game
from records import Records
from parametrs import *


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [-v=2] [-c=2] [-s=mini]",
        description="Pacman AI simulator"
    )
    parser.add_argument("-v", "--version", action="version", version=f"{parser.prog} version 1.0.0")

    parser.add_argument('-c', '--clever_enemies', type=int, dest="clever_enemies", default=2,
                        help='provide an integer (default: 2)')
    parser.add_argument('-d', '--dum_enemies', type=int, dest="dum_enemies", default=2,
                        help='provide an integer (default: 2)')
    parser.add_argument('-s', '--strategy', dest="strategy", choices=['mini', 'expecti'], default='expecti',
                        help='provide string value  (default: expecti)')
    return parser


class GameWindow:
    def __init__(self, screen):
        parser = init_argparse()
        args = parser.parse_args()
        self.strategy = args.strategy
        self.dum_enemies = args.dum_enemies
        self.clever_enemies = args.clever_enemies

        self.screen = screen

        self.records_page = False

        self.font = pygame.font.Font(None, 35)

        self.records = Records(RECORDS_PATH, self.clever_enemies, self.dum_enemies, self.strategy)
        self.game = Game(self.records, self.clever_enemies, self.dum_enemies, self.strategy)


    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:

                            return True

                elif event.key == pygame.K_ESCAPE:
                    if self.game.game_over:
                        self.game.score = 0
                    self.game.game_over = True
                    self.records_page = False

        return False

    def run_logic(self):
        self.game.run_logic()

    def display_frame(self) -> None:
        self.screen.fill(BLACK)
        if self.game.game_over:
            if self.game.score:
                message = 'You win' if self.game.win else 'You lose'
                self.display_message("Game Over! {} Final Score: {}".format(message, self.game.score), WHITE)
            else:
                sys.exit()
        else:
            self.game.draw_game(self.screen)

        pygame.display.flip()

    def display_message(self, message, color=RED) -> None:
        label = self.font.render(message, True, color)
        width = label.get_width()
        height = label.get_height()
        pos_x = SCREEN_WIDTH / 2 - width / 2
        pos_y = SCREEN_HEIGHT / 2 - height / 2
        self.screen.blit(label, (pos_x, pos_y))

