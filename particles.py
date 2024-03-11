import pygame
import math
import random
from pygame import Vector2, Rect
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
	def __init__(self, pos : Vector2 = Vector2(0, 0), time : int = 100, attributes : list = [], color : tuple = (255, 255, 255), size : float = 5.0):
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
			elif attributes[i][0] == "randSize":
				self.randSize(attributes[i][1] if len(attributes[i]) > 1 else 10)
			elif attributes[i][0] == "adjustSize":
				self.adjustSize(attributes[i][1] if len(attributes[i]) > 1 else [2, [3, 10]])
			else:
				pass

			#prints which attribute was applied. *Prints multiple times per frame depending on how many attributes there are.*
			# if attributes[i][0] != None:
			# 	print(f"applied {attributes[i][0]}.")
	
	'''
	draws the particle relative to the particle emitter.
	'''
	def draw(self, screen, emitterPos):
		pygame.draw.circle(screen, self.color, self.pos + emitterPos, math.floor(self.size))

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
		elif type(angles) == int: 
			self.angle = angles
		else:
			raise TypeError("type(angles) != list or int")

	'''
	- pow
	[pow is the velocity added when this function is called.]

	moves the particles based on the angle of the particle. This can be set in randAngle.
	'''
	def moveOnAngle(self, pow):
		self.velo += (math.cos(math.radians(self.angle)) * (pow/10), math.sin(math.radians(self.angle)) * (pow/10))

	'''
	- range
	[range is the range of possible sizes that particles can be set to.]
	[range can be set to an int, in which case all random sizes will be within 1 and range.]
	
	sets the size of the particle to a random size.
	'''
	def randSize(self, range):
		if type(range) == list:
			self.size = random.randint(range[0], range[1])
		elif type(range) == int:
			self.size = random.randint(1, range)
		else:
			raise TypeError("type(range) != list or int")
	
	'''
	- settings = [pow, minMax]
	[pow is the amount you want to adjust size by each frame.]
	[minMax is the minimum and maximum size you can have a particle be.]

	randomly adjusts the size of the particle each frame.

	to achieve a linear increase, set pow to a single number instead of a list.
	specific ranges can be set by inputing ranges such as [-200, 154].
	'''
	def adjustSize(self, settings):
		pow = settings[0]
		minMax = settings[1]
		scale = 1

		#sets all minMax values depending on type(minMax)
		if type(minMax) == list:
			min = minMax[0]
			max = minMax[1]
		elif type(minMax) == float or type(minMax) == int:
			min = 1
			max = minMax
		else:
			raise TypeError("type(minMax) != list, float, or int")
		
		#sets the minPow and maxPow depending on type(pow)
		if type(pow) == list:
			minPow, maxPow = pow[0], pow[1]
		elif type(pow) == float or type(pow) == int:
			minPow, maxPow = pow, pow
		else:
			raise TypeError("type(pow) != list, float, or int")
		
		#gets the correct scaling to handle with random values. This allows for ranges of .0005 to .01 for example.
		if type(minPow) == float or type(maxPow) == float:
			#this code gets the length of the number after the decimal. It's then able to have scale set to the largest one of the two lengths.
			try:
				minPowScale = 10**len(str(minPow).split(".")[1])
			except:
				minPowScale = 0
			try:
				maxPowScale = 10**len(str(maxPow).split(".")[1])
			except:
				maxPowScale = 0
			scale = minPowScale if minPowScale > maxPowScale else maxPowScale
		
		self.size += random.randint(minPow * scale, maxPow * scale)/scale
			
		#limits size to minMax values
		if self.size < min:
			self.size = min
		elif self.size > max:
			self.size = max
			
class ParticleEmitter:
	'''
	Attribute list:
		randYVelo
		randXVelo
		gravity
		randAngle
		moveOnAngle
		randSize
		adjustSize
	
	[ppf is particles per frame.]
	[particle time is the lifetime of the particles]
	[liveParticleAttributes is the attributes you apply to the particles when updating them.]
		[possible attributes include: randXVelo, randYVelo, gravity, randAngle, and moveOnAngle.]
	[initParticleAttributes is the attributes you apply to the particles when initializing them.]
		[possible attributes are the same as for liveParticleAttributes.]
	'''
	def __init__(self, pos = Vector2(0, 0), maxParticles = 10, ppf = 1, particleTime = 100, particleColors : tuple = (255, 255, 255), liveParticleAttributes = [["randXVelo", 5], ["gravity", [100, .25]]], initParticleAttributes = []): #ppf = particles per frame
		self.pos = pos
		self.maxParticles = maxParticles
		self.particleList = []
		self.ppf = ppf
		self.particleTime = particleTime
		self.particleColors = particleColors
		self.liveParticleAttributes = liveParticleAttributes
		self.initParticleAttributes = initParticleAttributes

	def update(self, screen, pos = None):
		'''if the particle emitter is moved, this is where it updates self.pos.'''
		if pos != None: 
			self.pos = pos

		'''new particles are set up here. If the maximum particles has been reached, no new particles will be added.'''
		for i in range(self.ppf):
			if len(self.particleList) <= self.maxParticles:
				self.particleList.append(Particle(Vector2(0, 0), self.particleTime, self.initParticleAttributes, self.particleColors))

		'''loops through and updates all particles in the list.'''
		for i in range(len(self.particleList)-1, 0, -1):
			'''updates the particles and passes the update attributes.'''
			self.particleList[i].update(screen, self.pos, self.liveParticleAttributes)
			'''removes the particles if they aren't on screen, or if their lifetime has run out.'''
			'''the collide rect is set to the screen, adjusted for the size of the particle'''
			collideRect = Rect(SCREEN_RECT.x - self.particleList[i].size, SCREEN_RECT.y - self.particleList[i].size, SCREEN_RECT.w + (self.particleList[i].size * 2), SCREEN_RECT.h + (self.particleList[i].size * 2))
			if self.particleList[i].time == 0 or not collideRect.collidepoint(self.particleList[i].pos + self.pos):
				del self.particleList[i]