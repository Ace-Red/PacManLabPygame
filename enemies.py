import random

import pygame

from entity import Entity
from parameters import *


class Spirit(pygame.sprite.Sprite, Entity):
    def __init__(self, image_path, grid):
        pygame.sprite.Sprite.__init__(self)
        Entity.__init__(self, grid)
        self.change_x = 0
        self.change_y = 0
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = self.get_random_start_position()
        self.change_direction()

        self.intersection_position = self.get_intersection_position()

    def update(self):
        self.rect.x += self.change_x
        self.rect.y += self.change_y
        if self.rect.right < 0:
            self.rect.left = SCR_WIDTH
        elif self.rect.left > SCR_WIDTH:
            self.rect.right = 0
        if self.rect.bottom < 0:
            self.rect.top = SCR_HEIGHT
        elif self.rect.top > SCR_HEIGHT:
            self.rect.bottom = 0

        if self.rect.topleft in self.intersection_position:
            self.change_direction()

    def change_direction(self):

        direction = random.choice(self.get_available_directions())
        if direction == "left":
            self.change_x = -2
            self.change_y = 0
        elif direction == "right":
            self.change_x = 2
            self.change_y = 0
        elif direction == "up":
            self.change_x = 0
            self.change_y = -2
        elif direction == "down":
            self.change_x = 0
            self.change_y = 2

    def get_available_directions(self):
        gen_x = len(self.grid)
        gen_y = len(self.grid[0])
        j = self.rect.topleft[0] // BLOCK_SIZE
        i = self.rect.topleft[1] // BLOCK_SIZE
        directions = []
        if self.grid[(i + 1) % gen_x][j] != 0:
            directions.append('down')
        if self.grid[(i - 1) % gen_x][j] != 0:
            directions.append('up')
        if self.grid[i][(j + 1) % gen_y] != 0:
            directions.append('right')
        if self.grid[i][(j - 1) % gen_y] != 0:
            directions.append('left')
        return directions

    def get_intersection_position(self):
        items = set()
        for i, row in enumerate(self.grid):
            for j, item in enumerate(row):
                if item != 0 and not is_tube(get_cell_neighbours(self.grid, i, j)):
                    items.add((j * BLOCK_SIZE, i * BLOCK_SIZE))

        return items


def is_tube(neighbours):
    return len(list(filter(lambda x: x != 0, neighbours))) == 2 and (
            (neighbours[0] != 0 and neighbours[1] != 0) or (neighbours[2] != 0 and neighbours[3] != 0))


def get_cell_neighbours(grid, x, y):
    gen_x = len(grid)
    gen_y = len(grid[0])
    neighbours = [grid[(x + 1) % gen_x][y], grid[(x - 1) % gen_x][y], grid[x][(y + 1) % gen_y],
                  grid[x][(y - 1) % gen_y]]
    return neighbours


class Blinky(Spirit):

    def __init__(self, grid):
        super().__init__('image/blinky.png', grid)


class Clyde(Spirit):

    def __init__(self, grid):
        super().__init__('image/clyde.png', grid)


class Inky(Spirit):

    def __init__(self, grid):
        super().__init__('image/inky.png', grid)


class Pinky(Spirit):

    def __init__(self, grid):
        super().__init__('image/pinky.png', grid)
