from timeit import default_timer as timer

import pygame.mixer

from enemies import Inky, Pinky
from entity import Block, Ellipse
from environment import generate_environment, draw_environment
from player import Player, ExpectPacman
from parametrs import *


class Game(object):

    def __init__(self, records, clever_enemies=2, dum_enemies=2, strategy='mini'):
        self.records = records

        self.game_over = False
        self.win = False
        self.life = MAX_LIFE_LEVEL
        self.font = pygame.font.Font(None, 35)
        self.score = 0
        self.level = 1
        self.grid = generate_environment()
        self.empty_blocks = pygame.sprite.Group()
        self.non_empty_blocks = pygame.sprite.Group()
        self.dots_group = pygame.sprite.Group()
        self.start = timer()

        for i, row in enumerate(self.grid):
            for j, item in enumerate(row):
                if item == 0:
                    self.empty_blocks.add(
                        Block(j * BLOCK_SIZE + 8, i * BLOCK_SIZE + 8, BLACK, HALF_BLOCK_SIZE + 4, HALF_BLOCK_SIZE + 4))
                else:
                    self.non_empty_blocks.add(
                        Block(j * BLOCK_SIZE + QUARTER_BLOCK_SIZE, i * BLOCK_SIZE + QUARTER_BLOCK_SIZE, BLACK,
                              HALF_BLOCK_SIZE, HALF_BLOCK_SIZE))
                    self.dots_group.add(Ellipse(j * BLOCK_SIZE + 12, i * BLOCK_SIZE + 12, WHITE, QUARTER_BLOCK_SIZE,
                                                QUARTER_BLOCK_SIZE))

        self.enemies = pygame.sprite.Group()
        self.player = Player(self.grid, self.dots_group, self.enemies) if strategy == 'mini' \
            else ExpectPacman(self.grid, self.dots_group, self.enemies)

        block = pygame.sprite.spritecollide(self.player, self.non_empty_blocks, False)[0]
        self.player_i = int((block.rect.y - QUARTER_BLOCK_SIZE) // BLOCK_SIZE)
        self.player_j = int((block.rect.x - QUARTER_BLOCK_SIZE) // BLOCK_SIZE)

        for x in range(clever_enemies):
            self.enemies.add(Inky(self.grid, self.player_i, self.player_j))
        for x in range(dum_enemies):
            self.enemies.add(Pinky(self.grid, self.player_i, self.player_j))

    def run_logic(self):
        if not self.game_over:
            self.player.update(self.empty_blocks)
            block_hit_list = pygame.sprite.spritecollide(self.player, self.dots_group, True)
            if len(block_hit_list) > 0:
                self.score += len(block_hit_list)
            if self.life > 1:
                block_hit_list = pygame.sprite.spritecollide(self.player, self.enemies, False)
                if len(block_hit_list) > 0:
                    self.decrease_life_level()
            else:
                block_hit_list = pygame.sprite.spritecollide(self.player, self.enemies, True)
                if len(block_hit_list) > 0:
                    self.life = 0
                    self.player.explosion = True
            self.game_over = self.player.game_over

            blocks = pygame.sprite.spritecollide(self.player, self.non_empty_blocks, False)
            if len(blocks) != 0:
                self.player_i = int((blocks[0].rect.y - QUARTER_BLOCK_SIZE) // BLOCK_SIZE)
                self.player_j = int((blocks[0].rect.x - QUARTER_BLOCK_SIZE) // BLOCK_SIZE)

            self.enemies.update(self.player_i, self.player_j)
            if len(self.dots_group) == 0:
                self.increase_level()

            if self.level == MAX_LEVEL + 1:
                self.game_over = True
                self.win = True
            if self.game_over:
                end = timer()
                time = round(end - self.start, 3)
                self.records.add_score(self.score, self.win, time)

    def decrease_life_level(self):
        self.life -= 1
        self.player = Player(self.grid, self.dots_group, self.enemies)

    def increase_level(self):
        level = self.level + 1
        score = self.score
        life = self.life
        self.__init__(self.records)
        self.level = level
        self.life = life
        self.score = score
        self.game_over = False

    def draw_game(self, screen):
        draw_environment(screen, self.grid)
        self.dots_group.draw(screen)
        self.enemies.draw(screen)
        screen.blit(self.player.image, self.player.rect)
        text = self.font.render("Score: {}; HP: {}".format(self.score, self.life), True, WHITE)
        screen.blit(text, [120, 20])
