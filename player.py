import pygame
from pygame.math import Vector2
import math
from math import atan2
from pygame import Rect

class Player:

	def __init__(self,scale):
		#load image
		self.baseImage = pygame.image.load('resources/guyNice.png')
		self.baseBlaster = pygame.image.load('resources/bigfist.png')
		#give images correct sizes (96 pixels and 75 pixels respectively)
		self.defaultSizeImage = pygame.transform.smoothscale_by(self.baseImage,96/self.baseImage.get_rect().height)
		self.defaultSizeBlaster = pygame.transform.smoothscale_by(self.baseBlaster, 75/self.baseBlaster.get_rect().width)
		#scales images to resolution
		self.image = pygame.transform.smoothscale_by(self.defaultSizeImage,scale)
		self.BlasterImage = pygame.transform.smoothscale_by(self.defaultSizeBlaster,scale)

		#self.transformed_image = pygame.transform.rotate(self.image, 0)
		self.transformed_Blaster = pygame.transform.rotate(self.BlasterImage, 0)
		
		self.vel = Vector2(0,0)
		self.centerpos = Vector2(400,400)

		self.newMousePos = Vector2(0,0)
		self.oldMousePos = Vector2(0,0)
		self.correctionangle = 90
		self.mouseVels: list[Vector2] = []
	
	def mouseMove(self,delta):
		self.newMousePos = Vector2(pygame.mouse.get_pos())

	
	def rotate(self):
		angle = math.degrees(math.atan2( self.newMousePos.x-self.centerpos.x, self.newMousePos.y-self.centerpos.y))+180
		
		self.transformed_Blaster = pygame.transform.rotate(self.BlasterImage, angle)
	
	def draw(self,screen):
		rect_to_draw = Rect(self.image.get_rect())
		rect_to_draw.center = (int(self.centerpos.x), int(self.centerpos.y))

		rect_to_blow = Rect(self.transformed_Blaster.get_rect())
		rect_to_blow.center = (int(self.centerpos.x), int(self.centerpos.y))

		screen.blit(
			self.transformed_Blaster,
			rect_to_blow
		)
		screen.blit(
			self.image,
			rect_to_draw 
		)

	def playerInput(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_a]:
			self.vel.x = -3
		if keys[pygame.K_d]:
			self.vel.x = 3
		if not keys[pygame.K_a] and not keys[pygame.K_d]:
			self.vel.x = 0

	def move(self,delta):
		self.centerpos+=self.vel
		
	def update(self,delta,screen):
		self.playerInput()
		self.move(delta)
		self.mouseMove(delta)
		self.rotate()
		self.draw(screen)
