import pygame
import math
import random
from pygame import Vector2, Rect
from globals import SCREEN_SIZE, SCREEN_RECT

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
	def __init__(self, pos : Vector2 = Vector2(0, 0), velo : Vector2 = Vector2(0, 0), emitterPos : Vector2 = Vector2(100, 100), time : int = 100, attributes : list = [], color : tuple = (255, 255, 255), size : float = 5.0, maxVelo : Vector2 = Vector2(100, 100), maxVeloAdjust : list = [-5, 5], veloType : str = "avg"):
		self.pos = pos + emitterPos
		self.velo = Vector2(0, 0) - velo/2
		self.color = color
		self.initColor = color
		self.time = time
		self.lifetime = time
		self.emitterPos = emitterPos
		self.size = size
		self.initSize = size
		self.angle = 0
		self.delta = 1
		self.maxVelo = maxVelo
		self.maxVeloAdjust = maxVeloAdjust
		self.delete = False
		self.veloType = veloType
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
		#distance values shouldn't have to be the same as emitterPos, and instead should be handled slightly differently.
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
			#drag could have different x and y settings.
			"drag" : self.drag,
			"dragOverLife" : self.dragOverLife,
			#could have all size functions (except for randSize) have size be relative to the init size if relativeSize var == True?
			#could also have size values passed as None and then they would just be treated as the current size value.
			"randSize" : self.randSize,
			"randAdjustSize" : self.randAdjustSize, #could add it so that it's min and max are relative to your init size.
			"sizeOverLife" : self.sizeOverLife,
			"sizeOverDistance" : self.sizeOverDistance,
			"sizeOverVelo" : self.sizeOverVelo,
			"randColor" : self.randColor,
			"randAdjustColor" : self.randAdjustColor, #could add it so that it's min and max (along side (0, 0, 0), and (255, 255, 255)) are relative to init color.
			#colors could be set to None, and then they would default to the init color.
			#could have all color functions be relative to the init color if relativeColor var == True?
			#if a color value which should be a tuple is an int, it could be set to the black and white color of that value. so if 100 is inputed, a color of (100, 100, 100) would be returned.
			"colorOverLife" : self.colorOverLife,
			"colorOverDistance" : self.colorOverDistance,
			"colorOverVelo" : self.colorOverVelo,
			"deleteOnColor" : self.deleteOnColor,
			"deleteOnVelo" : self.deleteOnVelo,
			"deleteOnSize" : self.deleteOnSize,
			"deleteOnDistance" : self.deleteOnDistance,
			"spreadOverVelo" : None, #should apply different randVelo attributes depending on the velocity.
			}
		defaultSettings = {
			"randYVelo" : 5,
			"randXVelo" : 5,
			"randVelo" : 5,
			"gravity" : .25,
			"randAngle" : [0, 360],
			"moveOnAngle" : 5,
			"drag" : [.15, .2],
			"dragOverLife" : [.15, .2, .5, 1, 5],
			"randSize" : 10,
			"randAdjustSize" : [2, [3, 10]],
			"sizeOverLife" : [1, 10, 5, 10, 1],
			"sizeOverDistance" : [100, [1, 10, 5, 10, 1]],
			"sizeOverVelo" : [10, [1, 15]],
			"randColor" : [(255, 255, 255)],
			"randAdjustColor" : [10, [(0, 0, 0), (255, 255, 255)]],
			"colorOverLife" : [(255, 255, 255), (0, 0, 0)],
			"colorOverDistance" : [100, [(0, 0, 0), (255, 255, 255)]],
			"colorOverVelo" : [self.maxVelo.x if self.maxVelo.x > self.maxVelo.y else self.maxVelo.y, [(0, 0, 0), (255, 255, 255)]],
			"deleteOnColor" : (0, 0, 0),
			"deleteOnVelo" : 0,
			"deleteOnSize" : 0,
			"deleteOnDistance" : 100,
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

	'''
	- color
	- createList

	Defines color based on the type of color.
	CreateList will create a list even if the inputed color is just a single color. (defaulting to [self.initColor, inputedColor]).
	If color is none, the color will be self.color at init.
	If it's an int/float, it will be a black and white version of that color.
	If it's an (r, g, b) color, it will stay that color.
	A list of colors can be inputted as well.
	'''
	def defineColor(self, color, createList):
		def define(definingColor):
			if definingColor == None:
				return self.initColor
			elif type(definingColor) == int or type(definingColor) == float:
				return (definingColor, definingColor, definingColor)
			elif type(definingColor) == tuple:
				return definingColor
			else:
				raise TypeError(f"The inputed color != int, float, None, or tuple. type(color) == {type(definingColor)}")
			
		if type(color) == list:
			tempList = []
			for i in range(len(color)):
				tempList.append(define(color[i]))
			return tempList
		elif createList:
			return[self.initColor, define(color)]
		else:
			return define(color)

	'''
	- color
	- minColor
	- maxColor

	caps the color values of color to minColor and maxColor values.
	'''
	def capColor(self, color, minColor, maxColor):
		cappedColor = [0, 0, 0]
		for i in range(3):
			if color[i] < minColor[i]:
				cappedColor[i] = (minColor[i])
			elif color[i] > maxColor[i]:
				cappedColor[i] = (maxColor[i])
			else:
				cappedColor[i] = (color[i])

		return (cappedColor[0], cappedColor[1], cappedColor[2])

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
		elif type(pow) == int or type(pow) == float:
			powMin, powMax = -pow, pow
		else:
			raise TypeError(f"Pow is not an int, float, or list. type(pow) = {type(pow)}")
		
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
		elif type(pow) == int or type(pow) == float:
			powMin, powMax = -pow, pow
		else:
			raise TypeError(f"Pow is not an int, float, or list. type(pow) = {type(pow)}")
		
		self.velo += Vector2(randfloat(powMin, powMax)/10, 0)

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
			self.angle = randfloat(minAngle, maxAngle)
		elif type(angles) == int or type(angles) ==  float: 
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
	def randSize(self, sizeRange):
		if type(sizeRange) == list:
			self.size = randfloat(sizeRange[0], sizeRange[1])
		elif type(sizeRange) == int or type(sizeRange) == float:
			self.size = randfloat(1, sizeRange)
		else:
			raise TypeError(f"type(sizeRange) != list, float, or int. type(range) = {type(sizeRange)}")
	
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
		minMaxSize = settings[1]

		#sets all minMax values depending on type(minMax)
		if type(minMaxSize) == list:
			minSize = minMaxSize[0]
			maxSize = minMaxSize[1]
		elif type(minMaxSize) == int or type(minMaxSize) == float:
			minSize = 1
			maxSize = minMaxSize
		else:
			raise TypeError(f"type(minMax) != list, float, or int. type(minMax) = {type(minMaxSize)}")
		
		#sets the minPow and maxPow depending on type(pow)
		if type(pow) == list:
			minPow, maxPow = pow[0], pow[1]
		elif type(pow) == int or type(pow) == float:
			minPow, maxPow = -pow, pow
		else:
			raise TypeError(f"type(pow) != list, float, or int. type(pow) = {type(pow)}")
		
		self.size += randfloat(minPow, maxPow)
			
		#limits size to minMax values
		if self.size < minSize:
			self.size = minSize
		elif self.size > maxSize:
			self.size = maxSize

	'''
	- endSize
	[endSize is the size that the particle will have when it's lifetime has reached 0.]

	Linearly scales particle size between the size at init, and endSize.
	'''
	def sizeOverLife(self, sizeRange):
		if type(sizeRange) == int or type(sizeRange) == float:
			sizes = [self.initSize, sizeRange]
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
			sizes = [self.initSize, sizeRange]
		elif type(sizeRange) == list:
			sizes = sizeRange
		else:
			raise TypeError(f"type(sizeRange) != list or type. sizeRange = {sizeRange}, which is a {type(sizeRange)}.")
		
		sizePercent = abs(math.sqrt((self.pos.x - self.emitterPos.x)**2 + (self.pos.y - self.emitterPos.y)**2)/maxDist)
		self.percentInList(sizes, sizePercent, self.moveBetweenSizes)

	'''
	- settings[maxVelo, veloType, sizeRange]
	[maxVelo is the velocity at which the final color is determined.]
	[veloType is the way that the sizes are calculated. The types are avg and dom.]
		[dom is the most dominate velocity of x and y.]
		[avg is the average velocity between x and y.]
	[sizeRange must be at least one int/float, but specific values can be set with a list of any number more ints/floats.]
	[sizeRange doesn't have a maximum amount of specific sizes to cycle through, and will display all sizes from left to right based on the velocity of the particle.]

	Interpolates between size values based on the velocity of the particle.
	'''
	def sizeOverVelo(self, settings):
		maxVelo = settings[0]
		sizeRange = settings[1]
		veloType = self.veloType if len(settings) < 3 else settings[2]

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
	- settings[velo, minDistance, veloType]
	[velo is the velo that you want to delete the particle on.]
	[minDistance is the minimum distance from color required to delete the particle.]
	[minDistance is an optional setting, and settings can be passed just as velo alone. eg. 2instead of [2, 5]]

	deletes the particle if it's velo is equal to the velo passed to this function.
	'''
	def deleteOnVelo(self, settings):
		if type(settings) == list:
			velo = settings[0]
			minDistance = settings[1]
			veloType = self.veloType if len(settings) < 3 else settings[2]
		elif type(settings) == int or type(settings) == float:
			velo = settings
			minDistance = 2
			veloType = self.veloType
		
		if veloType == "avg":
			veloDistance = (abs(self.velo.x) + abs(self.velo.y))/2
		elif veloType == "dom":
			veloDistance = abs(self.velo.x) if abs(self.velo.x) > abs(self.velo.y) else abs(self.velo.y)
		else:
			raise NameError(f"{veloType} isn't a veloType option.")

		if veloDistance < minDistance:
			self.deleteParticle()

	'''
	- settings[colorRange, colorType]
	[colorRange must be at least one (rgb) tuple, but specific values can be set with a list of two (rgb) tuples.]
	[colorType is optional, and will default to color, but if set to monotone, colorType will randomly pick equally from all color ranges.]

	Randomly selects a color from a range of colors.
	'''
	def randColor(self, settings):
		if type(settings) == list:
			colorRange = self.defineColor(settings[0], True)
			randType = settings[1]
		elif type(settings) == tuple or type(settings) == int or type(settings) == float or settings == None:
			colorRange = self.defineColor(settings, True)
			randType = "color"
		else:
			raise TypeError(f"Settings not set propperly. Settings should be a list, tuple, int, float, or None. type(settings) == {type(settings)}")
		
		#sorts the colors so that whichever values are smallest ARE SMALLEST. and whichever are biggest, ARE BIGGEST.
		tempMin= colorRange[0]
		tempMax = colorRange[1]
		minColor = (tempMin[0] if tempMin[0] < tempMax[0] else tempMax[0], tempMin[1] if tempMin[1] < tempMax[1] else tempMax[1], tempMin[2] if tempMin[2] < tempMax[2] else tempMax[2])
		maxColor = (tempMax[0] if tempMax[0] > tempMin[0] else tempMin[0], tempMax[1] if tempMax[1] > tempMin[1] else tempMin[1], tempMax[2] if tempMax[2] > tempMin[2] else tempMin[2])
		
		if randType == "monotone":
			val = random.randint(0, 100)/100
			r = math.floor((maxColor[0] - minColor[0]) * val + minColor[0])
			g = math.floor((maxColor[1] - minColor[1]) * val + minColor[1])
			b = math.floor((maxColor[2] - minColor[2]) * val + minColor[2])
			self.color = (r, g, b)
			self.color = self.capColor(self.color, minColor, maxColor)
		elif randType == "color":
			self.color = (random.randint(minColor[0], maxColor[0]), random.randint(minColor[1], maxColor[1]), random.randint(minColor[2], maxColor[2]))
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
		minMaxColor = self.defineColor(settings[1])

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
				minColor = minMaxColor[0][i]
				maxColor = minMaxColor[1][i]
			elif type(settings[1]) == tuple:
				minColor = 0
				maxColor = minMaxColor[1][i]
			else:
				raise TypeError("type(pow) != list or tuple")
			if self.color[i] < minColor:
				minMaxAdjustList[i] = minColor
			elif self.color[i] > maxColor:
				minMaxAdjustList[i] = maxColor
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
		colors = self.defineColor(colorRange, True)

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
		colors = self.defineColor(settings[1], True)

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
		colors = self.defineColor(settings[1], True)
		veloType = self.veloType if len(settings) < 3 else settings[2]

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
			color = self.defineColor(settings[0])
			minDistance = settings[1]
		elif type(settings) == tuple:
			color = self.defineColor(settings)
			minDistance = 5
		if self.colorDistance(self.color, color) < minDistance:
			self.deleteParticle()

	'''
	- settings[size, minDistance]
	[size is the size that you want to delete the particle on.]
	[minDistance is the minimum distance from size required to delete the particle.]
	[minDistance is an optional setting, and settings can be passed just as size alone. eg. 0 instead of [0, 1]]

	deletes the particle if it's size is equal to the size passed to this function.
	'''
	def deleteOnSize(self, settings):
		if type(settings) == list:
			size = settings[0]
			minDistance = settings[1]
		elif type(settings) == tuple:
			size = settings
			minDistance = 1
		if abs(self.size - size) < minDistance:
			self.deleteParticle()

	'''
	- minDistance
	[minDistance is the minimum distance from size required to delete the particle.]

	deletes the particle if it's distance is more than minDistance.
	'''
	def deleteOnDistance(self, minDistance):
		if abs(math.sqrt((self.emitterPos.x - self.pos.x)**2 + (self.emitterPos.y - self.pos.y)**2)) > minDistance:
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
		if type(dragRange) != list: TypeError(f"dragRange != list, type(dragRange) == {type(dragRange)}")
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
	def __init__(self, pos = Vector2(0, 0), updateAttributes : list = [["randXVelo", 5], ["gravity", .25], ["colorOverLife", [(255, 255, 255), (255, 255, 255), (0, 0, 0)]]], initAttributes : list = [], maxParticles : int = 100, ppf : float = 1, particleLifetime : int = 100, color : tuple = (255, 255, 255), size : float = 10, maxVelo = Vector2(100, 150), maxVeloAdjust = 5, cull : bool = True, veloType : str = "avg"): #ppf = particles per frame
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
		self.veloType = veloType
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
				self.particleList.append(Particle(Vector2(0, 0), velo, self.pos, self.particleLifetime, self.initAttributes, self.color, self.size, self.maxVelo, self.maxVeloAdjust, self.veloType))

		'''loops through and updates all particles in the list.'''
		for i in range(len(self.particleList)-1, 0, -1):
			'''updates the particles and passes the update attributes.'''
			self.particleList[i].update(screen, self.updateAttributes, delta = self.delta, emitterPos = self.pos)
			'''removes the particles if they aren't on screen, or if their lifetime has run out.'''
			'''the collide rect is set to the screen, adjusted for the size of the particle'''
			currentParticle = self.particleList[i]
			collideRect = Rect(SCREEN_RECT.x - currentParticle.size, SCREEN_RECT.y - currentParticle.size, SCREEN_RECT.w + (currentParticle.size * 2), SCREEN_RECT.h + (currentParticle.size * 2))
			if (self.particleList[i].time == 0) or (currentParticle.delete) or (type(self.cull) == bool and (not collideRect.collidepoint(currentParticle.pos) and self.cull)) or (type(self.cull) == list and ((currentParticle.pos.y + currentParticle.size < 0 and self.cull[0]) or (currentParticle.pos.x - currentParticle.size > SCREEN_SIZE[0] and self.cull[2]) or (currentParticle.pos.y - currentParticle.size > SCREEN_SIZE[1] and self.cull[3]) or (currentParticle.pos.x + currentParticle.size < 0 and self.cull[1]))):
				del self.particleList[i]