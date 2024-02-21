import pygame
from globals import FPS, SCREEN_SIZE
from boss import Boss
from player import Player
pygame.init()

doExit = False
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_SIZE))

boss = Boss((400, 400))
guy = Player(1)
while not doExit:
	delta = clock.tick(FPS) / 1000
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			doExit = True #lets you quit program
	screen.fill((0, 0, 0))
	
	boss.update(screen)
	guy.update(delta,screen)
	pygame.display.flip()
pygame.quit()