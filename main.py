import pygame
from pygame import Vector2
from particles import ParticleEmitter
from globals import FPS, SCREEN_SIZE
from boss import Boss
from player import Player
pygame.init()

doExit = False
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_SIZE))

testParticleEmitter = ParticleEmitter(Vector2(SCREEN_SIZE)//2, 100, 1)

boss = Boss((400, 400))
guy = Player(1)
while not doExit:
	delta = clock.tick(FPS) / 1000
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			doExit = True #lets you quit parogram
	screen.fill((0, 0, 0))

	testParticleEmitter.update(screen)
	
	boss.update(screen)
	guy.update(delta,screen)
	pygame.display.flip()
pygame.quit()