import pygame
import math
from pygame import locals as pg
from .car import Car
from .colors import red, white

class AICar(Car):
    ray_angles = [-90,-60, -45, -25, -15, -7.5, 0, 7.5, 15, 25, 45, 60, 90]
    def __init__(self, in_id: int = -1):
        super().__init__(in_id)
        self.rays = []
        self.ray_points = []
        
    #def update(self):
    #    self.apply_controls(self.brain.decision(self.rays, self.speed, self.angle))
    #    self.rotation()
    #    self.movement()

    def check_ray(self, track,  max_length, ray_angle):
        length = 0
        _sin = math.sin(math.radians(self.angle + ray_angle))
        _cos = math.cos(math.radians(self.angle + ray_angle))

        while length < max_length:
            length += 1
            x = self.x + _sin * length
            y = self.y - _cos * length
            if track.is_wall(x,y):
                break

        return length, x, y

    def check_rays(self, track, draw = False, max_length = 300):
        self.rays = []
        self.ray_points = []
        for ray_angle in AICar.ray_angles:
            distance, x, y = self.check_ray(track, max_length, ray_angle)
            intensity = 1 - distance / max_length
            self.rays.append(intensity)
            self.ray_points.append([x,y])     

    def draw(self, surface, draw_rays = True):
        super().draw(surface)
        if draw_rays:
            for point in self.ray_points:
                pygame.draw.line(surface, white, self.rect.center, point, 1)
                pygame.draw.circle(surface, red, point, 3)
