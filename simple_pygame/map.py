from dataclasses import dataclass
import pygame
from pygame import locals as pg
import json

grey = pygame.Color(128, 128, 128)  

@dataclass 
class Point:
    x: float = 0
    y: float = 0
    def __init__(self,ix=0,iy=0):
        self.x, self.y = ix, iy

@dataclass 
class Track:
    filepath: str
    starting_point: Point
    starting_angle: int
    def __init__(self,path,ix=0,iy=0, iangle = 0):
        self.filepath = path
        self.starting_point = Point(ix,iy)
        self.starting_angle = iangle

maps = { 
    "oval": Track("./tracks/01_oval.png",880,400, 90),
    "stadium" : Track("./tracks/02_stadium.png",350,170, 180),
 }

class Map():
    def __init__(self, window, map_name = "stadium"):
        self.window = window
        self.name = map_name
        self.surface = pygame.image.load(maps[self.name].filepath).convert_alpha()
        self.wall_mask = pygame.mask.from_surface(self.surface)
    def get_starting_position(self):
        start = maps[self.name].starting_point
        return start.x, start.y
    def get_starting_angle(self):
        return maps[self.name].starting_angle
    def check_collision(self, player):
        return self.wall_mask.overlap(player.mask, player.rect.topleft) is not None
    def draw(self, display, color, thickness):
        display.blit(self.surface, (0, 0))


class EmptyMap():
    def __init__(self, window):
        self.window = window
        self.outer_walls = window.get_rect().inflate(-10, -10)
    def get_starting_position(self):
        w, h = self.window.get_size()
        return w/2, h - 150
    def check_collision(self, player):
        return not self.outer_walls.contains(player.rect)
    def draw(self, display, color, thickness):
        pygame.draw.rect(display, color, self.outer_walls, 2)

