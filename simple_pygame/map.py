import pygame
from pygame import locals as pg

grey = pygame.Color(128, 128, 128)  


class Map():
    def __init__(self, window):
        self.window = window
        pass
    def get_starting_position(self):
        pass
    def check_collision(self, rect):
        pass


class EmptyMap(Map):
    def __init__(self, window):
        self.window = window
        self.outer_walls = window.get_rect().inflate(-10, -10)
    def get_starting_position(self):
        w, h = self.window.get_size()
        return w/2, h - 150
    def check_collision(self, rect):
        return not self.outer_walls.contains(rect)
    def draw(self, display, color, thickness):
        pygame.draw.rect(display, color, self.outer_walls, 2)

