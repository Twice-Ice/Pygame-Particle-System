#https://stackoverflow.com/questions/19968066/pygame-set-alpha-level-for-shapes

import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600), 0, 32)

surface1 = pygame.Surface((100,100))
surface1.set_colorkey((0,0,0))
surface1.set_alpha(128)
pygame.draw.circle(surface1, (0,255,0), (50,50), 50)

surface2 = pygame.Surface((100,100))
surface2.set_colorkey((0,0,0))
surface2.set_alpha(128)
pygame.draw.circle(surface2, (255,0,0), (50,50), 50)

screen.blit(surface1, (100,100))
screen.blit(surface2, (120,120))

pygame.display.update()

RUNNING = True

while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False

pygame.quit()