import pygame

black = (0, 0, 0)
pygame.init()
WIDTH = 606
HEIGHT = 606
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('PacMan')
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(black)
clock = pygame.time.Clock()


def startGame():
    done = False
    while done == False:

        clock.tick(10)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                done = True

        screen.fill(black)

        pygame.display.flip()


startGame()
pygame.quit()
