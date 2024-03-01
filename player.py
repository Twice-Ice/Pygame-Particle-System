import pygame
from pygame.math import Vector2
import math
from math import atan2
from pygame import Rect
from bullet import Homing

class Player:
	''':)'''
	def __init__(self,scale):
		self.delta:float
		self.screen: pygame.Surface
		###load image
		self.baseImage = pygame.image.load('resources/guyNice.png')
		self.baseBlaster = pygame.image.load('resources/bigfist.png')
		###give images correct sizes (96 pixels and 75 pixels respectively)
		self.defaultSizeImage = pygame.transform.smoothscale_by(self.baseImage,96/self.baseImage.get_rect().height)
		self.defaultSizeBlaster = pygame.transform.smoothscale_by(self.baseBlaster, 75/self.baseBlaster.get_rect().width)
		###scales images to resolution
		self.image = pygame.transform.smoothscale_by(self.defaultSizeImage,scale)
		self.BlasterImage = pygame.transform.smoothscale_by(self.defaultSizeBlaster,scale)

		#self.transformed_image = pygame.transform.rotate(self.image, 0)
		self.transformed_Blaster = pygame.transform.rotate(self.BlasterImage, 0)
		
		self.vel = Vector2(0,0)
		self.centerpos = Vector2(400,400)

		self.newMousePos = Vector2(0,0)
		#self.oldMousePos = Vector2(0,0)
		#self.correctionangle = 90
		#self.mouseVels: list[Vector2] = []

		self.magicMissile = []
		self.cooldown = 0

		self.handAngle: float

	def mouseMove(self):
		self.newMousePos = Vector2(pygame.mouse.get_pos())

	
	def rotate(self):
		self.handAngle = math.degrees(math.atan2( self.newMousePos.x-self.centerpos.x, self.newMousePos.y-self.centerpos.y))+180
		
		self.transformed_Blaster = pygame.transform.rotate(self.BlasterImage, self.handAngle)
	
	def draw(self):
		rect_to_draw = Rect(self.image.get_rect())
		rect_to_draw.center = (int(self.centerpos.x), int(self.centerpos.y))

		rect_to_blow = Rect(self.transformed_Blaster.get_rect())
		rect_to_blow.center = (int(self.centerpos.x), int(self.centerpos.y))

		self.screen.blit(
			self.transformed_Blaster,
			rect_to_blow
		)
		self.screen.blit(
			self.image,
			rect_to_draw 
		)

	def playerInput(self):
		'''Gets Input from keyboard
		| Movement is pixels per second'''
		keys = pygame.key.get_pressed()
		###LEFT AND RIGHT
		if keys[pygame.K_a]:
			self.vel.x = -180
		if keys[pygame.K_d]:
			self.vel.x = 180
		if not keys[pygame.K_a] and not keys[pygame.K_d]:
			self.vel.x = 0
		###UP AND DOWN
		if keys[pygame.K_w]:
			self.vel.y = -180
		if keys[pygame.K_s]:
			self.vel.y = 180
		if not keys[pygame.K_w] and not keys[pygame.K_s]:
			self.vel.y = 0
		if keys[pygame.K_SPACE]:
			self.shoot()


	def move(self):
		'''Applies velocity to position'''
		self.centerpos+=self.vel*self.delta
	
	def shoot(self):
		if len(self.magicMissile)<3 and self.cooldown == 0:
			self.magicMissile.append(Homing(self.centerpos,90))
			self.cooldown+=0.0000000001

	def bullets(self):
		for i in range(len(self.magicMissile)):
			if i >= len(self.magicMissile):
				break
			self.magicMissile[i].target(self.newMousePos, self.delta)
			if (
			self.magicMissile[i].update(self.screen,self.delta)
			):
				self.magicMissile.pop(i)

	def update(self,delta,screen):
		'''Runs specific player functions every frame'''
		self.delta = delta
		self.screen = screen

		self.playerInput()
		self.move()
		self.mouseMove()
		self.rotate()
		self.draw()
		self.bullets()

		if self.cooldown != 0:
			self.cooldown+=1*delta
		if self.cooldown > 0.66:
			self.cooldown = 0