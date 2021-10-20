import pygame.mixer

from game import Game
from menu import Menu

from parametrs import *


class GameWindow(object):
    def __init__(self, screen):
        self.screen = screen

        self.records_page = False

        self.font = pygame.font.Font(None, 35)

        self.game = Game()

        self.menu = Menu(("Start", "Records", "Exit"), font_color=WHITE, font_size=60)

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            self.menu.event_handler(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.game.game_over and not self.records_page:
                        if self.menu.state == 0:
                            # start
                            self.game = Game(self.records)
                            self.game.game_over = False
                        elif self.menu.state == 1:
                            # records
                            self.records_page = True
                        elif self.menu.state == 2:
                            # exit
                            return True

                elif event.key == pygame.K_ESCAPE:
                    if self.game.game_over:
                        self.game.score = 0
                    else:
                        self.records.add_score(self.game.score)
                    self.game.game_over = True
                    self.records_page = False

        return False

    def run_logic(self):
        self.game.run_logic()

    def display_frame(self) -> None:
        # clear the screen
        self.screen.fill(BLACK)
        if self.game.game_over:
            if self.game.score:
                message = 'You win' if self.game.win else 'You lose'
                self.display_message("Game Over! {} Final Score: {}".format(message, self.game.score), WHITE)
            elif self.records_page:
                self.display_message_block(self.records.get_scores())
            else:
                self.menu.display_frame(self.screen)
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

    def display_message_block(self, message_block: [str]) -> None:
        if len(message_block) == 0:
            self.display_message(self.screen, 'No records')
            return

        number_of_messages = len(message_block)
        list_of_labels = list(map(lambda message: self.font.render(str(message), True, WHITE), message_block))
        height = list_of_labels[0].get_height() + 2

        pos_x = SCREEN_WIDTH * 0.3
        pos_y = SCREEN_HEIGHT / 2 - height * number_of_messages / 2

        for label in list_of_labels:
            self.screen.blit(label, (pos_x, pos_y))
            pos_y += height