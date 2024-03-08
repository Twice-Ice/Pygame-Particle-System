import pygame
import math
import random
from pygame import Vector2
from globals import SCREEN_RECT

class Particle:
	'''
	- pos
	- lifetime of particle
	- attributes for init
	- color of particle
	- size of particle

	The positions of the particles will be relative to the particle emitter instead of world coords
	Velo is set by default, but it can be updated and changed to different values within the attributes of the particle init.
	'''
	def __init__(self, pos : Vector2 = Vector2(0, 0), time : int = 100, attributes : list = [], color : tuple = (255, 255, 255), size : int = 5):
		self.pos = pos
		self.velo = Vector2(0, 0)
		self.color = color
		self.time = time
		self.size = size
		self.angle = 0
		self.applyAttributes(attributes)

	'''
	- screen to draw on
	- position of the emitter (in order to draw correctly.)
	- attributes of the particle upon updating.

	updates particles.
	'''
	def update(self, screen, emitterPos, attributes):
		self.time -= 1 #reduces the lifetime of the particle. This should probably be set to delta and adjusted by irl time instead of frame time but whatever.
		self.applyAttributes(attributes) #applies attributes
		self.updatePos() #updates the position of the particle based on self.velo
		self.draw(screen, emitterPos) #draws the particle to the screen.

	'''
	applies the attributes to the particle based on the list inputed to this function.
	this can be expanded and optimized.
	a dict would probably be best.
	'''
	def applyAttributes(self, attributes):
		for i in range(len(attributes)):
			if attributes[i][0] == "randYVelo":
				self.randYVelo(attributes[i][1] if len(attributes[i]) > 1 else 5)
			elif attributes[i][0] == "randXVelo":
				self.randXVelo(attributes[i][1] if len(attributes[i]) > 1 else 5)
			elif attributes[i][0] == "gravity":
				self.gravity(attributes[i][1] if len(attributes[i]) > 1 else [100, .25])
			elif attributes[i][0] == "randAngle":
				self.randAngle(attributes[i][1] if len(attributes[i]) > 1 else [0, 360])
			elif attributes[i][0] == "moveOnAngle":
				self.moveOnAngle(attributes[i][1] if len(attributes[i]) > 1 else 5)
			else:
				pass

			#prints which attribute was applied. *Prints multiple times per frame depending on how many attributes there are.*
			# if attributes[i][0] != None:
			# 	print(f"applied {attributes[i][0]}.")
	
	'''
	draws the particle relative to the particle emitter.
	'''
	def draw(self, screen, emitterPos):
		pygame.draw.circle(screen, self.color, self.pos + emitterPos, self.size)

	'''
	updates the position of the particle based on it's velo.
	'''
	def updatePos(self):
		self.pos += self.velo

	'''
	- vars
	[vars should contain the maximum fall speed as well as the change in velocity each frame.]

	applies gravity
	'''
	def gravity(self, vars):
		maxVelo = vars[0]
		pow = vars[1]
		if self.velo.y <= maxVelo:
			self.velo.y += pow
	
	'''
	- pow
	[pow can be a single integer which will set all the minimum power to - pow and positive for maximum pow.]
	[if pow is a list, minimum pow can be set manually and vice versa with maximum pow.]

	applies a random Y velocity to the particle. 
	'''
	def randYVelo(self, pow):
		if type(pow) == list:
			powMin, powMax = pow[0], pow[1]
		else:
			powMin, powMax = pow, pow
		self.velo += Vector2(0, random.randint(-powMin, powMax)/10)

	'''
	- pow
	[pow can be a single integer which will set all the minimum power to - pow and positive for maximum pow.]
	[if pow is a list, minimum pow can be set manually and vice versa with maximum pow.]

	applies a random X velocity to the particle. 
	'''
	def randXVelo(self, pow):
		if type(pow) == list:
			powMin, powMax = pow[0], pow[1]
		else:
			powMin, powMax = pow, pow
		self.velo += Vector2(random.randint(-powMin, powMax)/10, 0)

	'''
	- angles
	[angles can be set to an int. In this case, the angle will be set only to that value. If a desired result is 0 - angle, set that with a list of [0, angle]]
	[angles should be a list that contains the specific angles that can be set. This will allow for moveOnAngle to apply velocity based on a specific angle range.]
	
	sets a random angle for the particle. No velocity is applied in this function. Please refer to moveOnAngle to apply velocity based on angle.
	'''
	def randAngle(self, angles):
		if type(angles) == list:
			minAngle = angles[0]
			maxAngle = angles[1]
			self.angle = random.randint(minAngle, maxAngle)
		else: 
			self.angle = angles

	'''
	- pow
	[pow is the velocity added when this function is called.]

	moves the particles based on the angle of the particle. This can be set in randAngle.
	'''
	def moveOnAngle(self, pow):
		self.velo += (math.cos(self.angle) * (pow/10), math.sin(self.angle) * (pow/10))

class ParticleEmitter:
	'''
	- pos
	- maxParticles
	- ppf
	- particleTime
	- liveParticleAttributes
	- initParticleAttributes

	[ppf is particles per frame.]
	[particle time is the lifetime of the particles]
	[liveParticleAttributes is the attributes you apply to the particles when updating them.]
		[possible attributes include: randXVelo, randYVelo, gravity, randAngle, and moveOnAngle.]
	[initParticleAttributes is the attributes you apply to the particles when initializing them.]
		[possible attributes are the same as for liveParticleAttributes.]
	'''
	def __init__(self, pos = Vector2(0, 0), maxParticles = 10, ppf = 1, particleTime = 100, liveParticleAttributes = [["randXVelo", 5], ["gravity", [100, .25]]], initParticleAttributes = []): #ppf = particles per frame
		self.pos = pos
		self.maxParticles = maxParticles
		self.particleList = []
		self.ppf = ppf
		self.particleTime = particleTime
		self.liveParticleAttributes = liveParticleAttributes
		self.initParticleAttributes = initParticleAttributes

	def update(self, screen, pos = None):
		'''if the particle emitter is moved, this is where it updates self.pos.'''
		if pos != None: 
			self.pos = pos

		'''new particles are set up here. If the maximum particles has been reached, no new particles will be added.'''
		for i in range(self.ppf):
			if len(self.particleList) <= self.maxParticles:
				self.particleList.append(Particle(Vector2(0, 0), self.particleTime, self.initParticleAttributes))

		'''loops through and updates all particles in the list.'''
		for i in range(len(self.particleList)-1, 0, -1):
			'''updates the particles and passes the update attributes.'''
			self.particleList[i].update(screen, self.pos, self.liveParticleAttributes)
			'''removes the particles if they aren't on screen, or if their lifetime has run out.'''
			if self.particleList[i].time == 0 or not SCREEN_RECT.collidepoint(self.particleList[i].pos + self.pos):
				del self.particleList[i]