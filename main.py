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

testParticleEmitter = ParticleEmitter(
	pos = Vector2(SCREEN_SIZE)//2,
	# celeste :)
	# updateAttributes = [["colorOverLife", [(91, 206, 250), (91, 206, 250), (0, 0, 0), (245, 169, 184), (245, 169, 184), (0, 0, 0), (255, 255, 255), (255, 255, 255), (0, 0, 0), (245, 169, 184), (245, 169, 184), (0, 0, 0), (91, 206, 250), (91, 206, 250)]]],
	# initAttributes = [["randAngle"], ["moveOnAngle", 20]],
	# fire
	# updateAttributes = [["colorOverLife", [(0, 0, 0), (100, 20, 200), (255, 75, 20), (255, 100, 50), (255, 125, 50), (255, 200, 75)]], ["randVelo", 2], ["gravity", -.025], ["randYVelo", [0, 1]]],
	# initAttributes = [["randAngle", [310, 320]], ["moveOnAngle", 40]],
	updateAttributes = [["gravity", .02], ["colorOverVelo", [10, "dom", [(0, 0, 0), (100, 20, 200), (255, 75, 20), (255, 100, 50), (255, 125, 50), (255, 200, 75)]]]],
	initAttributes = [["randAngle"], ["moveOnAngle", 20]],
	maxParticles = 1000,
	ppf = 5,
	particleLifetime = 1000,
	# maxVelo = Vector2(),
	# color = (255, 255, 255),
	size = 10
	)

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