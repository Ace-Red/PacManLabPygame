import pygame

black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
purple = (255, 0, 255)
yellow = (255, 255, 0)

pygame.init()
WIDTH = 606
HEIGHT = 606
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('PacMan')
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(black)
clock = pygame.time.Clock()


class Wall(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height, color):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x


def setupRoom(all_sprites_list):
    wall_list = pygame.sprite.RenderPlain()

    walls = [[0, 0, 6, 600],
             [0, 0, 600, 6],
             [0, 600, 606, 6],
             [600, 0, 6, 606],
             [300, 0, 6, 66],
             [60, 60, 186, 6],
             [360, 60, 186, 6],
             [60, 120, 66, 6],
             [60, 120, 6, 126],
             [180, 120, 246, 6],
             [300, 120, 6, 66],
             [480, 120, 66, 6],
             [540, 120, 6, 126],
             [120, 180, 126, 6],
             [120, 180, 6, 126],
             [360, 180, 126, 6],
             [480, 180, 6, 126],
             [180, 240, 6, 126],
             [180, 360, 246, 6],
             [420, 240, 6, 126],
             [240, 240, 42, 6],
             [324, 240, 42, 6],
             [240, 240, 6, 66],
             [240, 300, 126, 6],
             [360, 240, 6, 66],
             [0, 300, 66, 6],
             [540, 300, 66, 6],
             [60, 360, 66, 6],
             [60, 360, 6, 186],
             [480, 360, 66, 6],
             [540, 360, 6, 186],
             [120, 420, 366, 6],
             [120, 420, 6, 66],
             [480, 420, 6, 66],
             [180, 480, 246, 6],
             [300, 480, 6, 66],
             [120, 540, 126, 6],
             [360, 540, 126, 6]
             ]

    for item in walls:
        wall = Wall(item[0], item[1], item[2], item[3], green)
        wall_list.add(wall)
        all_sprites_list.add(wall)

    return wall_list


class Player(pygame.sprite.Sprite):
    change_x = 0
    change_y = 0

    def __init__(self, x, y, filename):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(filename).convert()

        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
        self.prev_x = x
        self.prev_y = y

    def prevdirection(self):
        self.prev_x = self.change_x
        self.prev_y = self.change_y

    def changespeed(self, x, y):
        self.change_x += x
        self.change_y += y

    def update(self, walls):

        old_x = self.rect.left
        new_x = old_x + self.change_x

        self.rect.left = new_x

        old_y = self.rect.top
        new_y = old_y + self.change_y

        x_collide = pygame.sprite.spritecollide(self, walls, False)
        if x_collide:

            self.rect.left = old_x

        else:

            self.rect.top = new_y

            y_collide = pygame.sprite.spritecollide(self, walls, False)
            if y_collide:
                self.rect.top = old_y


w = 303 - 16
p_h = (7 * 60) + 19


def startGame():
    done = False
    all_sprites_list = pygame.sprite.RenderPlain()
    wall_list = setupRoom(all_sprites_list)

    pacman_collide = pygame.sprite.RenderPlain()
    pacman = Player(w, p_h, "pacman.png")
    all_sprites_list.add(pacman)
    pacman_collide.add(pacman)
    while done == False:

        clock.tick(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pacman.changespeed(-30, 0)
                if event.key == pygame.K_RIGHT:
                    pacman.changespeed(30, 0)
                if event.key == pygame.K_UP:
                    pacman.changespeed(0, -30)
                if event.key == pygame.K_DOWN:
                    pacman.changespeed(0, 30)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    pacman.changespeed(30, 0)
                if event.key == pygame.K_RIGHT:
                    pacman.changespeed(-30, 0)
                if event.key == pygame.K_UP:
                    pacman.changespeed(0, 30)
                if event.key == pygame.K_DOWN:
                    pacman.changespeed(0, -30)
        pacman.update(wall_list)

        screen.fill(black)
        wall_list.draw(screen)

        all_sprites_list.draw(screen)
        pygame.display.flip()


startGame()
pygame.quit()
