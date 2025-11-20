import pygame
from settings import *
from gameworld import *
from objects import *
pygame.init()

#Test123
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("StarHawk")

clock = pygame.time.Clock()
world = GameWorld(WIDTH, HEIGHT)

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                world.shoot()

    world.update()
    world.draw(screen)

    pygame.display.flip()

pygame.quit()
