import pygame
import math
import random
from pygame import Vector2
from globals import SCREEN_RECT

class Particle:
	def __init__(self, pos : Vector2 = Vector2(0, 0), time : int = 100, attributes : list = [], color : tuple = (255, 255, 255), size : int = 5): #these positions will be relative to the position of the particle emitter.
		self.pos = pos
		self.velo = Vector2(0, 0)
		self.color = color
		self.time = time
		self.size = size
		self.angle = 0
		self.applyAttributes(attributes)

	def update(self, screen, emitterPos, attributes):
		self.draw(screen, emitterPos)
		self.time -= 1
		self.applyAttributes(attributes)
		self.updatePos()

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
	
	def draw(self, screen, emitterPos):
		pygame.draw.circle(screen, self.color, self.pos + emitterPos, self.size)

	def updatePos(self):
		self.pos += self.velo

	def gravity(self, vars):
		maxVelo = vars[0]
		pow = vars[1]
		if self.velo.y <= maxVelo:
			self.velo.y += pow
	
	def randYVelo(self, pow):
		if type(pow) == list:
			powMin, powMax = pow[0], pow[1]
		else:
			powMin, powMax = pow, pow
		self.velo += Vector2(0, random.randint(-powMin, powMax)/10)

	def randXVelo(self, pow):
		if type(pow) == list:
			powMin, powMax = pow[0], pow[1]
		else:
			powMin, powMax = pow, pow
		self.velo += Vector2(random.randint(-powMin, powMax)/10, 0)

	def randAngle(self, angles : list):
		minAngle = angles[0]
		maxAngle = angles[1]
		self.angle = random.randint(minAngle, maxAngle)

	def moveOnAngle(self, pow):
		self.velo += (math.cos(self.angle) * (pow/10), math.sin(self.angle) * (pow/10))

class ParticleEmitter:
	def __init__(self, pos = Vector2(0, 0), maxParticles = 10, ppf = 1, particleTime = 100, liveParticleAttributes = [["randXVelo", 5], ["gravity", [100, .25]]], initParticleAttributes = []): #ppf = particles per frame
		self.pos = pos
		self.maxParticles = maxParticles
		self.particleList = []
		self.ppf = ppf
		self.particleTime = particleTime
		self.liveParticleAttributes = liveParticleAttributes
		self.initParticleAttributes = initParticleAttributes

	def update(self, screen, pos = None):
		if pos != None:
			self.pos = pos

		for i in range(self.ppf):
			if len(self.particleList) <= self.maxParticles:
				self.particleList.append(Particle(Vector2(0, 0), self.particleTime, self.initParticleAttributes))

		for i in range(len(self.particleList)-1, 0, -1):
			self.particleList[i].update(screen, self.pos, self.liveParticleAttributes)
			if self.particleList[i].time == 0 or not SCREEN_RECT.collidepoint(self.particleList[i].pos + self.pos):
				del self.particleList[i]