import math

import pygame

import Globals
from game_utils import blit_rotate_center
from game_utils import scaling_Images

class Car:

  My_car = scaling_Images(pygame.image.load("Images/red-car.png"), 0.6)
  IMG = My_car
  START_POS = (540, 560)

  def __init__(self, max_vel, rotation_vel):
      self.img = self.IMG
      self.max_vel = max_vel
      self.vel = 0
      self.rotation_vel = rotation_vel
      self.angle = 90
      self.x, self.y = self.START_POS
      self.acceleration = 0.02
      self.mask = pygame.mask.from_surface(self.img)
      self.finish_line = False
      self.middle = ((self.img.get_width()/2.0), (self.img.get_height()/2.0))

  def rotate(self, left=False, right=False):
      if left:
          self.angle += self.rotation_vel
      elif right:
          self.angle -= self.rotation_vel

  def draw(self, display):
      blit_rotate_center(display, self.img, (self.x, self.y), self.angle)

  def move_forward(self):
      self.vel = min(self.vel + self.acceleration, self.max_vel)
      if self.x < 0:
          self.x = 0
          Globals.SETBACK = True
      if self.x > 900:
          self.x = 900
          Globals.SETBACK = True
      if self.y < 0:
          self.y = 0
          Globals.SETBACK = True
      if self.y > 640:
          self.y = 640
          Globals.SETBACK = True
      self.move()

  def move(self):
      radians = math.radians(self.angle)
      vertical = math.cos(radians) * self.vel
      horizontal = math.sin(radians) * self.vel
      self.y -= vertical
      self.x -= horizontal

  def reduce_speed(self):
      self.vel = max(self.vel - self.acceleration /2, 0)
      self.move()

  def collide(self, mask, x=0, y=0):
      car_mask = pygame.mask.from_surface(self.img)
      offset = (int(self.x - x), int(self.y - y))
      poi = mask.overlap(car_mask, offset)
      return poi

  def bounce(self):
      self.vel = -self.vel
      self.move()

