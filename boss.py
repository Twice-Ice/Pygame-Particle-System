import pygame
import random
from bullet import Bullet
from pygame import Vector2

class Boss:
	def __init__(self, pos: tuple):
		self.pos = Vector2(pos)
		self.hp = 100
		self.stateList = ["idle", "follow"]
		self.currentState = "idle"
		self.ticker = 0
		self.bullets = []

	def draw(self, screen):
		height = 100
		width = 45
		pygame.draw.rect(screen, (255, 255, 255), (self.pos.x - width/2, self.pos.y - height/2, width, height))
		
	def move(self):
		pass

	def update(self, screen):
		self.ticker += 1
		if self.currentState == "idle":
			if self.ticker % 5 == 0:
				self.bullets.append(Bullet(self.pos, random.randint(0, 360), 5))

		for i in range(len(self.bullets)):
			self.bullets[i].update(screen)
		self.move()
		self.draw(screen)