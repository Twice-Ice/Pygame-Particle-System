import pygame
import math
from pygame import Rect
from globals import SCREEN_RECT
from pygame.math import Vector2

class Bullet:
    def __init__(self, pos:Vector2, angle:float, speed):
        self.pos = Vector2(pos)
        self.angle = float(angle)
        self.speed = speed

    def draw(self, screen):
        pygame.draw.circle(screen, (200, 50, 50), self.pos, 25)

    def move(self):
        self.pos.x += math.cos(self.angle) * self.speed
        self.pos.y += math.sin(self.angle) * self.speed

    def update(self, screen):
        if SCREEN_RECT.collidepoint(self.pos):
            self.move()
            self.draw(screen)
        else:
            del self