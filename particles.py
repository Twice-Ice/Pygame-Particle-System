import pygame
import math
import random
from pygame import Vector2, Vector3, Rect
from globals import SCREEN_RECT, SCREEN_SIZE

def randfloat(min, max):
	#gets the correct scaling to handle with random values. This allows for ranges of .0005 to .01 for example.
	scale = 10
	if type(min) == float or type(max) == float:
		#this code gets the length of the number after the decimal. It's then able to have scale set to the largest one of the two lengths.
		try:
			minScale = 10**len(str(min).split(".")[1])
		except:
			minScale = 0
		try:
			maxScale = 10**len(str(max).split(".")[1])
		except:
			maxScale = 0
		scale = minScale if minScale > maxScale else maxScale

	return random.randint(int(min * scale), int(max * scale))/scale

def moveBetweenColors(color1, color2, percent):
			r = math.floor((color2[0] - color1[0]) * percent + color1[0])
			g = math.floor((color2[1] - color1[1]) * percent + color1[1])
			b = math.floor((color2[2] - color1[2]) * percent + color1[2])
			return (r, g, b)

class Particle:
	'''
	- pos
	- lifetime of particle
	- attributes for init
	- color of particle
	- size of particle

	Velo is set by default, but it can be updated and changed to different values within the attributes of the particle init.
	'''
	def __init__(self, pos : Vector2 = Vector2(0, 0), velo : Vector2 = Vector2(0, 0), emitterPos : Vector2 = Vector2(100, 100), time : int = 100, attributes : list = [], color : tuple = (255, 255, 255), size : float = 5.0, maxVelo : Vector2 = Vector2(100, 100)):
		self.pos = pos + emitterPos
		self.velo = Vector2(0, 0) - velo/2
		self.color = color
		self.time = time
		self.lifetime = time
		self.emitterPos = emitterPos
		self.size = size
		self.angle = 0
		self.delta = 1
		self.maxVelo = maxVelo
		self.applyAttributes(attributes)

	'''
	- screen to draw on
	- position of the emitter (in order to draw correctly.)
	- attributes of the particle upon updating.

	updates particles.
	'''
	def update(self, screen, attributes, emitterPos, delta, velo : Vector2 = Vector2(0, 0)):
		self.time -= 1 #reduces the lifetime of the particle. This should probably be set to delta and adjusted by irl time instead of frame time but whatever.
		self.delta = delta
		self.emitterPos = emitterPos
		self.velo += velo
		self.applyAttributes(attributes) #applies attributes
		self.updatePos() #updates the position of the particle based on self.velo
		self.draw(screen) #draws the particle to the screen.

	'''
	applies the attributes to the particle based on the list inputed to this function.
	this can be expanded and optimized.
	a dict would probably be best.
	'''
	def applyAttributes(self, attributes):
		attributeFunctions = {
			"randYVelo" : self.randYVelo,
			"randXVelo" : self.randXVelo,
			"randVelo" : None,
			"gravity" : self.gravity,
			"randAngle" : self.randAngle,
			"moveOnAngle" : self.moveOnAngle,
			"randSize" : self.randSize,
			"adjustSize" : self.adjustSize,
			"sizeOverLife" : self.sizeOverLife,
			"sizeOverDistance" : None,
			"sizeOverVelo" : None,
			"randColor" : self.randColor,
			"adjustColor" : None,
			"colorOverLife" : self.colorOverLife,			
			"colorOverDistance" : self.colorOverDistance,
			"colorOverVelo" : self.colorOverVelo,
			"drag" : self.drag,
			"destroyOnColor" : None, #deletes the particle when it gets to a certain color?
			}
		defaultSettings = {
			"randYVelo" : 5,
			"randXVelo" : 5,
			"randVelo" : 5,
			"gravity" : .25,
			"randAngle" : [0, 360],
			"moveOnAngle" : 5,
			"randSize" : 10,
			"adjustSize" : [2, [3, 10]],
			"sizeOverLife" : 50,
			"sizeOverDistance" : None,
			"sizeOverVelo" : None,
			"randColor" : [(255, 255, 255)],
			"adjustColor" : None,
			"colorOverLife" : [(0, 0, 0), (255, 255, 255)],
			"colorOverDistance" : [100, [(0, 0, 0), (255, 255, 255)]],
			"colorOverVelo" : [100, "avg", [(0, 0, 0), (255, 255, 255)]],
			"drag" : [.15, .2],
			"destroyOnColor" : None,
		}
		for i in range(len(attributes)):
			default = attributes[i][1] if len(attributes[i]) > 1 else defaultSettings[attributes[i][0]]
			attributeFunctions[attributes[i][0]](default)
	
	'''
	draws the particle relative to the particle emitter.
	'''
	def draw(self, screen):
		pygame.draw.circle(screen, self.color, self.pos, math.floor(self.size))

	'''
	updates the position of the particle based on it's velo.
	velocity is capped here based on maxVelo.
	'''
	def updatePos(self):
		if self.velo.x > self.maxVelo.x: self.velo.x = self.maxVelo.x
		if self.velo.y > self.maxVelo.y: self.velo.y = self.maxVelo.y
		self.pos += self.velo * self.delta
		
	'''
	- pow
	[pow is the amount of velocity applied each frame this function is called.]

	applies gravity
	'''
	def gravity(self, pow):
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
			powMin, powMax = -pow, pow
		self.velo += Vector2(0, randfloat(powMin, powMax)/10)

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
		self.velo += Vector2(randfloat(-powMin, powMax)/10, 0)

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
		
		self.size += randfloat(minPow, maxPow)
			
		#limits size to minMax values
		if self.size < min:
			self.size = min
		elif self.size > max:
			self.size = max

	'''
	- endSize
	[endSize is the size that the particle will have when it's lifetime has reached 0.]

	Linearly scales particle size between the size at init, and endSize.
	'''
	def sizeOverLife(self, endSize):
		self.size += endSize/self.lifetime

	'''
	- settings[colorRange, colorType]
	[colorRange must be at least one (rgb) tuple, but specific values can be set with a list of two (rgb) tuples.]
	[colorType is optional, and will default to color, but if set to monotone, colorType will randomly pick equally from all color ranges.]

	Randomly selects a color from a range of colors.
	'''
	def randColor(self, settings):
		if type(settings) == list:
			colorRange = settings[0]
			try:
				randType = settings[1]
			except:
				randType = "color"
		else:
			raise TypeError(f"Settings not set properly.\nSettings should include color values as well as the type of random color.\nSuch as \"monotone,\" the 2nd index can be left blank and the type will default to colored.")
		if type(colorRange) == list:
			color1 = colorRange[0]
			color2 = colorRange[1]
		elif type(colorRange) == tuple:
			color1 = (0, 0, 0)
			color2 = colorRange
		else:
			raise TypeError(f"ColorRange != list or tuple, colorRange is a {type(colorRange)}")
		
		if randType == "monotone":
			val = random.randint(0, 100)/100
			r = math.floor((color2[0] - color1[0]) * val + color1[0])
			g = math.floor((color2[1] - color1[1]) * val + color1[1])
			b = math.floor((color2[2] - color1[2]) * val + color1[2])
			self.color = self.color + (r, g, b)
		elif randType == "color":
			self.color = (random.randint(color1[0], color2[0]), random.randint(color1[1], color2[1]), random.randint(color1[2], color2[2]))
		else:
			raise SyntaxError(f"{randType} for randType is not a valid option.")
		
	'''
	- colorRange
	[colorRange must be at least one (rgb) tuple, but specific values can be set with a list of any number more (rgb) tuples.]
	[colorRange doesn't have a maximum amount of specific colors to cycle through, and will display all colors from left to right throughout the lifespan of the particle.]

	Interpolates between color values over the lifespan of a particle.
	'''
	def colorOverLife(self, colorRange):
		if type(colorRange) == tuple:
			colors = [self.color, colorRange]
		elif type(colorRange) == list:
			colors = colorRange
		else:
			raise TypeError(f"type(colorRange) != list or tuple. colorRange = {colorRange}, which is a {type(colorRange)}.")

		for i in range(len(colors)-1):
			lifetimePercent = 1 - self.time/self.lifetime
			if lifetimePercent <= 1/(len(colors)-1) * (i + 1) and lifetimePercent > 1/(len(colors)-1) * i:
				self.color = moveBetweenColors(colors[i], colors[i+1], lifetimePercent * (len(colors) - 1) - i)

	'''
	- settings[maxDist, colorRange]
	[colorRange must be at least one (rgb) tuple, but specific values can be set with a list of any number more (rgb) tuples.]
	[colorRange doesn't have a maximum amount of specific colors to cycle through, and will display all colors from left to right based on the distance of the particle from it's emitter.]

	Interpolates between color values based on the distance of the particle from the particle's emitter.
	'''
	def colorOverDistance(self, settings):
		maxDist = settings[0]
		colorRange = settings[1]
		if type(colorRange) == tuple:
			colors = [self.color, colorRange]
		elif type(colorRange) == list:
			colors = colorRange
		else:
			raise TypeError(f"type(colorRange) != list or tuple. colorRange = {colorRange}, which is a {type(colorRange)}.")

		for i in range(len(colors)-1):
			lifetimePercent = abs(math.sqrt((self.pos.x - self.emitterPos.x)**2 + (self.pos.y - self.emitterPos.y)**2)/maxDist)
			if lifetimePercent == 0: lifetimePercent = 0.001
			elif lifetimePercent > 1: lifetimePercent = 1
			if lifetimePercent <= 1/(len(colors)-1) * (i + 1) and lifetimePercent > 1/(len(colors)-1) * i:
				self.color = moveBetweenColors(colors[i], colors[i+1], lifetimePercent * (len(colors) - 1) - i)

	'''
	- settings[maxVelo, veloType, colorRange]
	[maxVelo is the velocity at which the final color is determined.]
	[veloType is the way that the colors are calculated. The types are avg and dom.]
		[dom is the most dominate velocity of x and y.]
		[avg is the average velocity between x and y.]
	[colorRange must be at least one (rgb) tuple, but specific values can be set with a list of any number more (rgb) tuples.]
	[colorRange doesn't have a maximum amount of specific colors to cycle through, and will display all colors from left to right based on the velocity of the particle.]

	Interpolates between color values based on the velocity of the particle.
	'''
	def colorOverVelo(self, settings):
		maxVelo = settings[0]
		veloType = settings[1] if settings[1] != None else "avg"
		colorRange = settings[2]

		if type(colorRange) == tuple:
			colors = [self.color, colorRange]
		elif type(colorRange) == list:
			colors = colorRange
		else:
			raise TypeError(f"type(colorRange) != list or tuple. colorRange = {colorRange}, which is a {type(colorRange)}.")

		for i in range(len(colors)-1):
			if veloType == "avg":
				lifetimePercent = ((abs(self.velo.x) + abs(self.velo.y))/2)/maxVelo
			elif veloType == "dom":
				lifetimePercent = (abs(self.velo.x) if abs(self.velo.x) > abs(self.velo.y) else abs(self.velo.y))/maxVelo
			else:
				raise NameError(f"{veloType} isn't a color option.")
			if lifetimePercent <= 0: lifetimePercent = 0.01
			elif lifetimePercent >= 1: lifetimePercent = 1
			if lifetimePercent <= 1/(len(colors)-1) * (i + 1) and lifetimePercent > 1/(len(colors)-1) * i:
				self.color = moveBetweenColors(colors[i], colors[i+1], lifetimePercent * (len(colors) - 1) - i)

	'''
	- settings[pow, minVelo]
	[pow is the amount of drag applied each frame.]
	[minVelo is the minimum amount of velocity before setting the velo to 0. Make sure to keep minVelo > pow]

	Applies drag to the particle each frame.
	'''
	def drag(self, settings):
		pow = settings[0] * self.delta
		minVelo = settings[1] * self.delta
		if pow > minVelo: raise ValueError("pow > minVelo.")

		if abs(self.velo.x) < minVelo:
			self.velo.x = 0
		else:
			if self.velo.x < 0:
				self.velo.x += pow
			elif self.velo.x > 0:
				self.velo.x -= pow

		if abs(self.velo.y) < minVelo:
			self.velo.y = 0
		else:
			if self.velo.y < 0:
				self.velo.y += pow
			elif self.velo.y > 0:
				self.velo.y -= pow

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
	[updateAttributes is the attributes you apply to the particles when updating them.]
		[possible attributes include: randXVelo, randYVelo, gravity, randAngle, and moveOnAngle.]
	[initAttributes is the attributes you apply to the particles when initializing them.]
		[possible attributes are the same as for updateAttributes.]
	'''
	def __init__(self, pos = Vector2(0, 0), updateAttributes : list = [["randXVelo", 5], ["gravity", .25], ["colorOverLife", [(255, 255, 255), (255, 255, 255), (0, 0, 0)]]], initAttributes : list = [], maxParticles : int = 10, ppf : float = 1, particleLifetime : int = 100, color : tuple = (255, 255, 255), size : float = 10, maxVelo : Vector2 = Vector2(100, 100)): #ppf = particles per frame
		self.pos = pos
		self.maxParticles = maxParticles
		self.particleList = []
		self.ppf = ppf
		self.spawnParticle = 0
		self.delta = 1
		self.particleLifetime = particleLifetime
		self.color = color
		self.updateAttributes = updateAttributes
		self.initAttributes = initAttributes
		self.size = size
		self.maxVelo = maxVelo

	'''
	- screen
	- delta
	- pos
	- velo
	[screen is the screen to draw to.]
	[delta is deltatime. (fps/1000)]
	[pos is the position of where you want the emitter to be. If the pos is attached to a player for example, set pos as "player.pos" (or whatever your pos variable is named.)]
	[velo is the velocity of whatever your emitter is attached to/impacted by. This is very sensitive, so be careful to not apply too much force here.]

	Updates the emitter and every particle from the emitter. 
	'''
	def update(self, screen, delta = 1, pos = None, velo = None):
		'''if the particle emitter is moved, this is where it updates self.pos.'''
		if pos != None: 
			self.pos = Vector2(pos)
		if velo == None:
			velo = Vector2(0, 0)
		
		self.delta = delta + 1

		'''new particles are set up here. If the maximum particles has been reached, no new particles will be added.'''
		if self.ppf >= 1:
			for i in range(self.ppf):
				if len(self.particleList) <= self.maxParticles:
					self.particleList.append(Particle(Vector2(0, 0), velo, self.pos, self.particleLifetime, self.initAttributes, self.color, self.size, self.maxVelo))
		elif self.ppf < 1 and self.ppf >= 0:
			self.spawnParticle += self.ppf
			if self.spawnParticle > 1: 
				self.spawnParticle -= 1
				if len(self.particleList) <= self.maxParticles:
					self.particleList.append(Particle(Vector2(0, 0), velo, self.pos, self.particleLifetime, self.initAttributes, self.color, self.size, self.maxVelo))
		else:
			raise ValueError(f"self.ppf == {self.ppf}, which is less than 0")

		'''loops through and updates all particles in the list.'''
		for i in range(len(self.particleList)-1, 0, -1):
			'''updates the particles and passes the update attributes.'''
			self.particleList[i].update(screen, self.updateAttributes, delta = self.delta, emitterPos = self.pos)
			'''removes the particles if they aren't on screen, or if their lifetime has run out.'''
			'''the collide rect is set to the screen, adjusted for the size of the particle'''
			collideRect = Rect(SCREEN_RECT.x - self.particleList[i].size, SCREEN_RECT.y - self.particleList[i].size, SCREEN_RECT.w + (self.particleList[i].size * 2), SCREEN_RECT.h + (self.particleList[i].size * 2))
			if self.particleList[i].time == 0 or not collideRect.collidepoint(self.particleList[i].pos):
				del self.particleList[i]