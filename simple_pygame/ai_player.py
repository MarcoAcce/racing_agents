import pygame
import math
from pygame import locals as pg
from car import Car


class AICar(Car):
    ray_angles = [-90,-60, -45, -25, -15, -7.5, 0, 7.5, 15, 25, 45, 60, 90]
    def __init__(self, in_id: int = -1):
        super().__init__(in_id)

    #def update(self):
    #    self.apply_controls(self.brain.decision(self.rays))
    #    self.rotation()
    #    self.movement()

    def check_rays(self, track, draw = False, max_length = 300):
        self.rays = []
        collisions = []
        rays = []
        for ray_angle in AICar.ray_angles:
            ray_result = self.check_ray(track, max_length, ray_angle)
            intensity = 1 - ray_result[0] / max_length
            self.rays.append(intensity)     
            if draw:
                collisions.append([ray_result[1],ray_result[2]])
        return collisions

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

