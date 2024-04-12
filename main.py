import pygame
from pygame import Vector2
from particles import ParticleEmitter
from globals import FPS, SCREEN_SIZE
pygame.init()

doExit = False
clock = pygame.time.Clock()
screen = pygame.display.set_mode(SCREEN_SIZE)

fireFade = ParticleEmitter(
	pos = Vector2(SCREEN_SIZE)//2,
	updateAttributes = [
		["dragOverLife", [.15, .2, .2, .2, .5, 1, 5]],
		["sizeOverVelo", [6.5, [5, 6, 7, 8, 9, 9]]],
		["gravity", .02],
		["randVelo", 2.5],
		["deleteOnColor", [(0, 0, 0), 15]],
		["colorOverVelo", [6.5, [(0, 0, 0), (50, 10, 100), (255, 75, 20), (255, 100, 50), (255, 125, 50), (255, 200, 75)]]],
	],
	initAttributes = [
		["randAngle"],
		["moveOnAngle", 20],
		["randVelo", 15]
	],
	maxVelo = 15,
	maxVeloAdjust = 5,
	maxParticles = 1000,
	ppf = 7.5,
	particleLifetime = 1000,
	spawnType = "onMove",
	ppfMaxVelo = 2.5
)

transLight = ParticleEmitter(
	updateAttributes = [
		["colorOverDistance", [250, [
			(91, 206, 250),
			(91, 206, 250),
			(0, 0, 0),
			(245, 169, 184),
			(245, 169, 184),
			(0, 0, 0),
			(255, 255, 255),
			(255, 255, 255),
			(0, 0, 0),
			(245, 169, 184),
			(245, 169, 184),
			(0, 0, 0),
			(91, 206, 250),
			(91, 206, 250),
			(12, 12, 12)
		]]],
		["sizeOverLife", [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0]],
		["deleteOnSize", [0, 1]],
	],
	initAttributes = [
		["randAngle"],
		["moveOnAngle", 20]
	],
	particleLifetime = 250,
	maxParticles = 1000,
	ppf = 10,
)

snow = ParticleEmitter(
	updateAttributes = [
		["gravity", .05],
		["randAdjustSize", [2, [1, 4.5]]],
		["randXVelo", 5]
	],
	initAttributes = [
		["randVelo", [75, 10]]
	],
	particleLifetime = 500,
	maxParticles = 1000,
	ppf = 5,
	cull = [False, True, True, True],
)

spiderverseCircles = ParticleEmitter(
	updateAttributes = [
		["randAdjustColor", [50, [(0, 0, 0), (255, 25, 255)]]],
		["deleteOnVelo", [0, .25]],
		["sizeOverVelo", [10, [0, 50]]],
		["drag"],
	],
	initAttributes = [
		["randColor"],
		["randYVelo", 200],
	]
)

flashlight = ParticleEmitter(
	updateAttributes = [
		["sizeOverDistance", [250, [10, 9, 0]]],
		["colorOverLife", [(255, 255, 150), (255, 255, 200), (200, 200, 150)]],
	],
	initAttributes = [
		["randAngle"],
		["moveOnAngle", 50],
	],
	maxParticles = 1000,
	particleLifetime = 250,
	ppf = 10,
)

testEmitter = ParticleEmitter(
	ppf = 10,
	maxParticles = 1000,
	updateAttributes = [
		["randColor", [None, "color"]]
	],
	initAttributes = [
		["randAngle"],
		["moveOnAngle", 20],
	],
	maxVelo = Vector2(20, 20),
)

while not doExit:
	delta = clock.tick(FPS) / 1000
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			doExit = True #lets you quit parogram
	screen.fill((0, 0, 0))

	# testEmitter.update(screen, delta, pos = pygame.mouse.get_pos(), velo = -Vector2(pygame.mouse.get_rel())/7.5)
	# transLight.update(screen, delta, pos = pygame.mouse.get_pos(), velo = -Vector2(pygame.mouse.get_rel())/7.5)
	# flashlight.update(screen, delta, pos = pygame.mouse.get_pos())
	fireFade.update(screen, delta, pos = pygame.mouse.get_pos(), velo = -Vector2(pygame.mouse.get_rel())/7.5)
	# snow.update(screen, delta, pos = Vector2(SCREEN_SIZE[0]//2, -100))
	# spiderverseCircles.update(screen, delta, pos = pygame.mouse.get_pos())

	pygame.display.flip()
pygame.quit()