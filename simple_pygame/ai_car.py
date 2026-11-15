import pygame
import math
from .car import Car
from .colors import red, white

class AICar(Car):
    ray_angles = [-90,-60, -45, -25, -15, -7.5, 0, 7.5, 15, 25, 45, 60, 90]
    def __init__(self, in_id: int = -1):
        super().__init__(in_id)
        self.rays = []
        self.ray_points = []
        self.nex_action = 8
        
    def update(self):
        accelerate  = self.nex_action == 0 or self.nex_action == 1 or self.nex_action == 2
        brake       = self.nex_action == 3 or self.nex_action == 4 or self.nex_action == 5
        left        = self.nex_action == 0 or self.nex_action == 3 or self.nex_action == 6
        right       = self.nex_action == 1 or self.nex_action == 4 or self.nex_action == 7
        self.apply_controls(accelerate, brake, left, right)
        self.rotation()
        self.movement()
    
    def get_observations(self):
        return [*self.rays, self.speed/5]

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

    def check_rays(self, track, max_length):
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
