import pygame
from pygame import Vector2
from particles import ParticleEmitter
from globals import FPS, SCREEN_SIZE
import math
import random
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

# testEmitter = ParticleEmitter(
# 	ppf = 5,
# 	maxParticles = 1000,
# 	updateAttributes = [
# 		["gravity"],
# 		["colorOverLife", [(0, 255, 175), (0, 0, 0)]],
# 		["deleteOnColor", (0, 0, 0)],
# 		["sizeOverVelo", [50, [1, 5, 5, 10]]]
# 	],
# 	initAttributes = [
# 		["randVelo", 5],
# 		["gravity", 1]
# 	],
# )

# center = Vector2(SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2)
# angle = 0
# value = 0
# direction = True
# dist = 100
# ehfdhs = 10
# maxVal = random.randint(5, ehfdhs)
# tempPos = Vector2(center.x + math.cos(math.radians(angle))*dist, center.y + math.sin(math.radians(angle))*dist)

class circleEmitter:
	def __init__(self, pos : Vector2):
		self.emitter = ParticleEmitter(
			ppf = 1,
			maxParticles = 1000,
			updateAttributes = [
				["gravity"],
				["colorOverDistance", [250, [(255, 255, 255), (0, 0, 0)]]],
				["deleteOnColor", (0, 0, 0)],
				["sizeOverVelo", [5, [1, 5]]]
			],
			initAttributes = [
				["randVelo", 5],
				["gravity", 1]
			],
		)
		self.emitter.particleSpawns += random.randint(0, 100)/100
		center = pos
		self.pos = pos
		self.angle = random.randint(0, 360)
		self.value = 0
		self.direction = True
		self.lr = 1 if random.randint(0, 10) % 2 else -1
		self.dist = 100
		self.ehfdhs = 10
		self.maxVal = random.randint(5, self.ehfdhs)
		self.idk = random.randint(1, 5)
		self.tempPos = Vector2(center.x + math.cos(math.radians(self.angle))*self.dist, center.y + math.sin(math.radians(self.angle))*self.dist)

	def update(self, screen, delta):
		if self.direction:
			self.value += .25
		if self.value == self.maxVal:
			self.direction = False
		elif not self.direction:
			self.value -= .25
			if self.value == 0:
				self.direction = True
				self.maxVal = random.randint(5, self.ehfdhs)
		
		# pygame.draw.circle(screen, (25, 25, 25), self.pos, 100, 1)

		self.old = self.tempPos
		# self.angle += (self.value/2) * self.lr
		self.tempPos = Vector2(self.pos.x + math.cos(math.radians(self.angle))*self.dist, self.pos.y + math.sin(math.radians(self.angle))*self.dist)
		self.emitter.update(screen, delta, self.tempPos, Vector2((self.old - self.tempPos).x * self.idk, (self.old - self.tempPos).y * self.idk))
		# pygame.draw.circle(screen, (255, 0, 0), self.tempPos, 5)

theList = []

for i in range(500):
	theList.append(circleEmitter(Vector2(random.randint(0, SCREEN_SIZE[0]), random.randint(0, SCREEN_SIZE[1]))))

while not doExit:
	delta = clock.tick(FPS) / 1000
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			doExit = True #lets you quit parogram
	screen.fill((0, 0, 0))

	# testEmitter.update(screen, delta, pos = pygame.mouse.get_pos(), velo = -Vector2(pygame.mouse.get_rel())/7.5)
	# transLight.update(screen, delta, pos = pygame.mouse.get_pos(), velo = -Vector2(pygame.mouse.get_rel())/7.5)
	# flashlight.update(screen, delta, pos = pygame.mouse.get_pos())
	# fireFade.update(screen, delta, pos = pygame.mouse.get_pos(), velo = -Vector2(pygame.mouse.get_rel())/7.5)
	# snow.update(screen, delta, pos = Vector2(SCREEN_SIZE[0]//2, -100))
	# spiderverseCircles.update(screen, delta, pos = pygame.mouse.get_pos())
	# if direction:
	# 	value += .25
	# 	if value == maxVal:
	# 		direction = False
	# elif not direction:
	# 	value -= .25
	# 	if value == 0:
	# 		direction = True
	# 		maxVal = random.randint(5, ehfdhs)
	
	# pygame.draw.circle(screen, (25, 25, 25), center, 100, 1)

	# old = tempPos
	# angle += value/2
	# tempPos = Vector2(center.x + math.cos(math.radians(angle))*dist, center.y + math.sin(math.radians(angle))*dist)
	# testEmitter.update(screen, delta, tempPos, Vector2((old - tempPos).x * value, (old - tempPos).y * value))
	# pygame.draw.circle(screen, (255, 0, 0), tempPos, 5)

	for item in theList:
		item.update(screen, delta)

	pygame.display.flip()
pygame.quit()