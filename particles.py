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

class Particle:
	'''
	- pos
	- lifetime of particle
	- attributes for init
	- color of particle
	- size of particle

	Velo is set by default, but it can be updated and changed to different values within the attributes of the particle init.
	'''
	def __init__(self, pos : Vector2 = Vector2(0, 0), velo : Vector2 = Vector2(0, 0), emitterPos : Vector2 = Vector2(100, 100), time : int = 100, attributes : list = [], color : tuple = (255, 255, 255), size : float = 5.0, maxVelo : Vector2 = Vector2(100, 100), maxVeloAdjust : list = [-5, 5]):
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
		self.maxVeloAdjust = maxVeloAdjust
		self.delete = False
		self.applyAttributes(attributes)

	# MAIN FUNCTIONS

	'''
	- screen to draw on
	- position of the emitter (in order to draw correctly.)
	- attributes of the particle upon updating.

	updates particles.
	'''
	def update(self, screen, attributes, emitterPos, delta, velo : Vector2 = Vector2(0, 0)):
		self.time -= 1 #reduces the lifetime of the particle. This should probably be set to delta and adjusted by irl time instead of frame time but whatever.
		self.delta = delta #updates local deltatime for the particle.
		self.emitterPos = emitterPos #updates the emitter's position.
		self.velo += velo #adds the velo of the emitter.
		self.applyAttributes(attributes) #applies attributes.
		self.updatePos() #updates the position of the particle based on self.velo.
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
			"randVelo" : self.randVelo,
			"gravity" : self.gravity,
			"randAngle" : self.randAngle,
			"moveOnAngle" : self.moveOnAngle,
			"randSize" : self.randSize,
			"randAdjustSize" : self.randAdjustSize,
			"sizeOverLife" : self.sizeOverLife,
			"sizeOverDistance" : self.sizeOverDistance,
			"sizeOverVelo" : self.sizeOverVelo,
			"deleteOnVelo" : self.deleteOnVelo,
			"randColor" : self.randColor,
			"randAdjustColor" : self.randAdjustColor,
			"colorOverLife" : self.colorOverLife,			
			"colorOverDistance" : self.colorOverDistance,
			"colorOverVelo" : self.colorOverVelo,
			"deleteOnColor" : self.deleteOnColor,
			"drag" : self.drag,
			"dragOverLife" : self.dragOverLife,
			"spreadOverVelo" : None, #should apply different randVelo attributes depending on the velocity.
			}
		defaultSettings = {
			"randYVelo" : 5,
			"randXVelo" : 5,
			"randVelo" : 5,
			"gravity" : .25,
			"randAngle" : [0, 360],
			"moveOnAngle" : 5,
			"randSize" : 10,
			"randAdjustSize" : [2, [3, 10]],
			"sizeOverLife" : [1, 10, 5, 10, 1],
			"sizeOverDistance" : [100, [1, 10, 5, 10, 1]],
			"sizeOverVelo" : [10, "avg", [1, 15]],
			"deleteOnVelo" : 0,
			"randColor" : [(255, 255, 255)],
			"randAdjustColor" : [10, [(0, 0, 0), (255, 255, 255)]],
			"colorOverLife" : [(0, 0, 0), (255, 255, 255)],
			"colorOverDistance" : [100, [(0, 0, 0), (255, 255, 255)]],
			"colorOverVelo" : [100, "avg", [(0, 0, 0), (255, 255, 255)]],
			"deleteOnColor" : (0, 0, 0),
			"drag" : [.15, .2],
			"dragOverLife" : [.15, .2, .2, .2, .5, 1, 5],
			"spreadOverVelo" : None,
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
	
	a random adjust is applied when maxVelo is reached to avoid clumping. This can be changed by settings maxVeloAdjust in the emitter init. By default, it is set to 5.
	'''
	def updatePos(self):
		#the velocities are capped, but also have an added random value to avoid clumping if a large selection of particles all exeed maxVelo.
		if abs(self.velo.x) > self.maxVelo.x: self.velo.x = (self.maxVelo.x) * (self.velo.x/abs(self.velo.x)) + randfloat(self.maxVeloAdjust[0], self.maxVeloAdjust[1])
		if abs(self.velo.y) > self.maxVelo.y: self.velo.y = (self.maxVelo.y) * (self.velo.y/abs(self.velo.y)) + randfloat(self.maxVeloAdjust[0], self.maxVeloAdjust[1])
		self.pos += self.velo * self.delta

	# HELPER FUNCTIONS

	'''
	- color1
	- color2
	- percent

	sets self.color to an interpolated point between color1 and color2 based on the percent value.
	'''
	def moveBetweenColors(self, color1 : tuple, color2 : tuple, percent : float):
		r = math.floor((color2[0] - color1[0]) * percent + color1[0])
		g = math.floor((color2[1] - color1[1]) * percent + color1[1])
		b = math.floor((color2[2] - color1[2]) * percent + color1[2])
		self.color = (r, g, b)

	'''
	- size1
	- size2
	- percent

	sets self.size to an interpolated point between size1 and size2 based on the percent value.
	'''
	def moveBetweenSizes(self, size1 : float, size2 : float, percent : float):
		self.size = (size2 - size1) * percent + size1

	'''
	- list
	- percent
	- function
	[list is the list of possible values to interpolate between.]
	[percent is the total percent through the list.]
	[function is the function to use when setting the interpolated value.]

	in a list, finds the correct value out of a list of values to interpolate based on the total percent value.
	'''
	def percentInList(self, list : list, percent : float, function):
		for i in range(len(list)-1):
			if percent == 0: percent = 0.001
			elif percent >= .95: percent = 1
			if percent <= 1/(len(list)-1) * (i+1) and percent > 1/(len(list)-1) * i:
				function(list[i], list[i+1], percent * (len(list) - 1) - i)

	'''
	deletes self from particle emitter list.
	the actual del call is within the emitter when cycling through the list.
	'''
	def deleteParticle(self):
		self.delete = True
	
	'''
	- color1
	- color2

	calculates the distance between color1 and color2, and then averages them out.
	'''
	def colorDistance(self, color1, color2):
		colorDist = tuple(map(lambda i, j: i - j, color1, color2))
		return abs(sum(colorDist)/len(colorDist))

	# PARTICLE FUNCTIONS

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
	- pow
	[pow can be an int or a 2d list.]
	[as an int/float, all default values will be set to the range -pow, pow.]
	[as a 2d list, randXVelo and randYVelo can be set manually as [[xVeloSettings], [yVeloSettings]]]
	[xVeloSettings/yVeloSettings are structured the same as randXVelo/randYVelo]

	applies a random X and Y velocity to the particle.
	'''
	def randVelo(self, pow):
		if type(pow) == int or type(pow) == float:
			xRange = pow
			yRange = pow
		elif type(pow) == list:
			xRange = pow[0]
			yRange = pow[1]
		else:
			raise TypeError(f"pow (a {type(pow)}) != list or int.")
		
		self.randXVelo(xRange)
		self.randYVelo(yRange)

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
	def randAdjustSize(self, settings):
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
	def sizeOverLife(self, sizeRange):
		if type(sizeRange) == tuple:
			sizes = [self.size, sizeRange]
		elif type(sizeRange) == list:
			sizes = sizeRange
		else:
			raise TypeError(f"type(sizeRange) != list or type. sizeRange = {sizeRange}, which is a {type(sizeRange)}.")
		
		sizePercent = 1 - self.time/self.lifetime
		self.percentInList(sizes, sizePercent, self.moveBetweenSizes)

	'''
	- settings[maxDist, sizeRange]
	[maxDist is the maximum distance before the final size in sizeRange is reached.]
	[sizeRange as an int/float will interpolate sizes between it's starting size and the value you put for sizeRange.]
	[sizeRange as a list will contain all sizes that the size will interpolate between based on the particle's distance from it's emitter.]

	Interpolates between sizes of the particle based on the particle's distance from it's emitter.
	'''
	def sizeOverDistance(self, settings):
		maxDist = settings[0]
		sizeRange = settings[1]
		if type(sizeRange) == int or type(sizeRange) == float:
			sizes = [self.size, sizeRange]
		elif type(sizeRange) == list:
			sizes = sizeRange
		else:
			raise TypeError(f"type(sizeRange) != list or type. sizeRange = {sizeRange}, which is a {type(sizeRange)}.")
		
		sizePercent = abs(math.sqrt((self.pos.x - self.emitterPos.x)**2 + (self.pos.y - self.emitterPos.y)**2)/maxDist)
		self.percentInList(sizes, sizePercent, self.moveBetweenSizes)

	'''
	- settings[maxVelo, veloType, sizeRange]
	[maxVelo is the velocity at which the final color is determined.]
	[veloType is the way that the colors are calculated. The types are avg and dom.]
		[dom is the most dominate velocity of x and y.]
		[avg is the average velocity between x and y.]
	[sizeRange must be at least one int/float, but specific values can be set with a list of any number more ints/floats.]
	[sizeRange doesn't have a maximum amount of specific sizes to cycle through, and will display all sizes from left to right based on the velocity of the particle.]

	Interpolates between size values based on the velocity of the particle.
	'''
	def sizeOverVelo(self, settings):
		maxVelo = settings[0]
		veloType = settings[1] if settings[1] != None else "avg"
		sizeRange = settings[2]

		if type(sizeRange) == int or type(sizeRange) == float:
			sizes = [self.size, sizeRange]
		elif type(sizeRange) == list:
			sizes = sizeRange
		else:
			raise TypeError(f"type(sizeRange) != list or tuple. sizeRange = {sizeRange}, which is a {type(sizeRange)}.")
		
		if veloType == "avg":
			colorPercent = ((abs(self.velo.x) + abs(self.velo.y))/2)/maxVelo
		elif veloType == "dom":
			colorPercent = (abs(self.velo.x) if abs(self.velo.x) > abs(self.velo.y) else abs(self.velo.y))/maxVelo
		else:
			raise NameError(f"{veloType} isn't a color option.")
		
		self.percentInList(sizes, colorPercent, self.moveBetweenSizes)

	'''
	- settings[velo, minDistance]
	[velo is the velo that you want to delete the particle on.]
	[minDistance is the minimum distance from color required to delete the particle.]
	[minDistance is an optional setting, and settings can be passed just as velo alone. eg. 2instead of [2, 5]]

	deletes the particle if it's velo is equal to the velo passed to this function.
	'''
	def deleteOnVelo(self, settings):
		if type(settings) == list:
			velo = settings[0]
			minDistance = settings[1]
		elif type(settings) == tuple:
			velo = settings
			minDistance = 2
		if abs(self.velo - velo) <= minDistance:
			self.deleteParticle()

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
	- settings = [pow, minMax]
	[pow is the amount you want to adjust the color by each frame.]
	[minMax is the minimum and maximum color values you can have a particle be.]

	randomly adjusts the color of the particle each frame.

	to achieve a linear increase, set pow to a single color instead of a list of colors.
	specific ranges can be set by inputing ranges such as [(0, 0, 0), (255, 255, 255)].
	'''
	def randAdjustColor(self, settings):
		pow = settings[0]
		minMax = settings[1]

		#sets the minPow and maxPow depending on type(pow)
		if type(pow) == list:
			minPow, maxPow = pow[0], pow[1]
		elif type(pow) == float or type(pow) == int:
			minPow, maxPow = -pow, pow
		else:
			raise TypeError("type(pow) != list, float, or int")

		#adjusts the color by random values
		self.color = tuple(map(lambda i, j: i + j, self.color, (random.randint(minPow, maxPow), random.randint(minPow, maxPow), random.randint(minPow, maxPow))))
		
		#caps off each of the color values to be greater than or equal to min and less than or equal to max.
		minMaxAdjustList = [0, 0, 0]
		for i in range(3):
			if type(settings[1]) == list:
				min = minMax[0][i]
				max = minMax[1][i]
			elif type(settings[1]) == tuple:
				min = 0
				max = minMax[1][i]
			else:
				raise TypeError("type(pow) != list or tuple")
			if self.color[i] < min:
				minMaxAdjustList[i] = min
			elif self.color[i] > max:
				minMaxAdjustList[i] = max
			else:
				minMaxAdjustList[i] = self.color[i]

		self.color = (minMaxAdjustList[0], minMaxAdjustList[1], minMaxAdjustList[2])
			
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

		colorPercent = 1 - self.time/self.lifetime
		self.percentInList(colors, colorPercent, self.moveBetweenColors)

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

		colorPercent = abs(math.sqrt((self.pos.x - self.emitterPos.x)**2 + (self.pos.y - self.emitterPos.y)**2)/maxDist)
		self.percentInList(colors, colorPercent, self.moveBetweenColors)

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

		if veloType == "avg":
			colorPercent = ((abs(self.velo.x) + abs(self.velo.y))/2)/maxVelo
		elif veloType == "dom":
			colorPercent = (abs(self.velo.x) if abs(self.velo.x) > abs(self.velo.y) else abs(self.velo.y))/maxVelo
		else:
			raise NameError(f"{veloType} isn't a color option.")
		
		self.percentInList(colors, colorPercent, self.moveBetweenColors)

	'''
	- settings[color, minDistance]
	[color is the color that you want to delete the particle on.]
	[minDistance is the minimum distance from color required to delete the particle.]
	[minDistance is an optional setting, and settings can be passed just as color alone. eg. (255, 255, 255) instead of [(255, 255, 255), 5]]

	deletes the particle if it's color is equal to the color passed to this function.
	'''
	def deleteOnColor(self, settings):
		if type(settings) == list:
			color = settings[0]
			minDistance = settings[1]
		elif type(settings) == tuple:
			color = settings
			minDistance = 5
		if self.colorDistance(self.color, color) < minDistance:
			self.deleteParticle()

	'''
	- settings[pow, minVelo]
	[pow is the amount of drag applied each frame.]
	[minVelo is the minimum amount of velocity before setting the velo to 0. Make sure to keep minVelo > pow]
	[minVelo can be automatically set by not inputing settings as a list an only inputing pow. In this case, minVelo is 1.25x pow.]

	Applies drag to the particle each frame.
	'''
	def drag(self, settings):
		if type(settings) == int or type(settings) == float:
			pow = settings * self.delta
			minVelo = pow * 1.25
		elif type(settings) == list:
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

	'''
	- dragRange
	[dragRange is the range of possible drag values that you can apply based on the current life of the particle.]
	[dragRange's inputs carry the same settings as the default drag attribute.]
	[this means you can pass integers/floats just as dragRange = [1, 1, 2, 5, etc.], ]
	[or you can pass minVelo attributes such as dragRange = [[.25, .35], [1, 2], [.5, 1], etc.]]

	applies drag based on the current life value of the particle.
	'''
	def dragOverLife(self, dragRange):
		dragPercent = 1 - self.time/self.lifetime
		currentDrag = dragRange[int((dragPercent - dragPercent % (100/len(dragRange)/100))//(100/len(dragRange)/100))]
		self.drag(currentDrag)

class ParticleEmitter:
	'''
	Attribute list:
		randYVelo
		randXVelo
		gravity
		randAngle
		moveOnAngle
		randSize
		randAdjustSize
	
	[ppf is particles per frame.]
	[particle time is the lifetime of the particles]
	[updateAttributes is the attributes you apply to the particles when updating them.]
		[possible attributes include: randXVelo, randYVelo, gravity, randAngle, and moveOnAngle.]
	[initAttributes is the attributes you apply to the particles when initializing them.]
		[possible attributes are the same as for updateAttributes.]
	'''
	def __init__(self, pos = Vector2(0, 0), updateAttributes : list = [["randXVelo", 5], ["gravity", .25], ["colorOverLife", [(255, 255, 255), (255, 255, 255), (0, 0, 0)]]], initAttributes : list = [], maxParticles : int = 10, ppf : float = 1, particleLifetime : int = 100, color : tuple = (255, 255, 255), size : float = 10, maxVelo = Vector2(100, 100), maxVeloAdjust = 5, cull : bool = True): #ppf = particles per frame
		self.pos = pos
		self.maxParticles = maxParticles
		self.particleList = []
		self.ppf = ppf
		self.particleSpawns = 0
		self.delta = 1
		self.particleLifetime = particleLifetime
		self.color = color
		self.updateAttributes = updateAttributes
		self.initAttributes = initAttributes
		self.size = size
		if type(maxVelo) == Vector2:
			self.maxVelo = maxVelo
		elif type(maxVelo) == int or type(maxVelo) == float:
			self.maxVelo = Vector2(maxVelo, maxVelo)
		else:
			raise TypeError(f"type(maxVelo) != Vector2, int or float. type(maxVelo) == {type(maxVelo)}")
		if type(maxVeloAdjust) == list:
			self.maxVeloAdjust = maxVeloAdjust
		elif type(maxVeloAdjust) == int or type(maxVeloAdjust) == float:
			self.maxVeloAdjust = [-maxVeloAdjust, maxVeloAdjust]
		else:
			raise TypeError(f"type(maxVeloAdjust) != list, int or float. type(maxVeloAdjust) == {type(maxVeloAdjust)}")
		self.cull = cull

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
		self.particleSpawns += self.ppf
		for i in range(math.floor(self.particleSpawns)):
			self.particleSpawns -= 1
			if len(self.particleList) <= self.maxParticles:
				self.particleList.append(Particle(Vector2(0, 0), velo, self.pos, self.particleLifetime, self.initAttributes, self.color, self.size, self.maxVelo, self.maxVeloAdjust))

		'''loops through and updates all particles in the list.'''
		for i in range(len(self.particleList)-1, 0, -1):
			'''updates the particles and passes the update attributes.'''
			self.particleList[i].update(screen, self.updateAttributes, delta = self.delta, emitterPos = self.pos)
			'''removes the particles if they aren't on screen, or if their lifetime has run out.'''
			'''the collide rect is set to the screen, adjusted for the size of the particle'''
			collideRect = Rect(SCREEN_RECT.x - self.particleList[i].size, SCREEN_RECT.y - self.particleList[i].size, SCREEN_RECT.w + (self.particleList[i].size * 2), SCREEN_RECT.h + (self.particleList[i].size * 2))
			if self.particleList[i].time == 0 or self.particleList[i].delete or (not collideRect.collidepoint(self.particleList[i].pos) and self.cull):
				del self.particleList[i]