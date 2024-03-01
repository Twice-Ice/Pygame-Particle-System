import pygame
import math
from pygame import Rect
from globals import SCREEN_RECT
from pygame.math import Vector2

class Bullet:
	def __init__(self, startpos:Vector2, speed:int = 1000, size:int = 10):
		self.startpos = Vector2(startpos)
		self.pos = Vector2(self.startpos)
		self.vel = Vector2(0,0)
		self.speed = speed
		self.size = size

	def draw(self, screen):
		pygame.draw.circle(screen, (200, 50, 50), self.pos, self.size)
	
	def move(self,delta):
		self.pos+=self.vel*self.speed*delta

	def update(self, screen,delta):
		if SCREEN_RECT.collidepoint(self.pos):
			self.move(delta)
			self.draw(screen)
		else:
			return True

class Homing(Bullet):
	def __init__(self, startpos: Vector2, speed: int = 100, size: int = 10):
		super().__init__(startpos, speed, size)
		
	def target(self,endpos:Vector2, delta: float):
		# drag_val = delta * 20
		# self.vel *= 1 - drag_val # drag
		self.vel += (endpos-self.pos).normalize() * 0.9
		
		if (
			abs(self.pos.x) <= abs(endpos.x) + self.size and
			abs(self.pos.x) >= abs(endpos.x) - self.size and
			abs(self.pos.y) <= abs(endpos.y) + self.size and
			abs(self.pos.y) >= abs(endpos.y) - self.size
		):
			return True
