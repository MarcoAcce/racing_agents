import pygame
import math
from pygame import locals as pg


class Player(pygame.sprite.Sprite):
    def __init__(self, in_id: int = -1):
        super().__init__()

        image = pygame.image.load('Car.png')
        self.original_image = pygame.transform.scale(image, (60, 100))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.x, self.y = 0, 0
        self.rect.center = (self.x, self.y)
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 0
        self.angle = 0
        self.id: int = in_id

    def rotation(self):
        if self.angle >= 360:
            self.angle = self.angle - 360
        if self.angle < 0:
            self.angle = 360 + self.angle
        self.image = pygame.transform.rotate(self.original_image,-self.angle)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=self.rect.center)

    def movement(self):
        angle_rad = math.radians(self.angle)
        hor = math.sin(angle_rad)*self.speed
        ver = -math.cos(angle_rad)*self.speed
        self.x += hor
        self.y += ver
        self.rect.center = (self.x, self.y)

    def update(self):
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pg.K_UP]:
            self.speed = min(self.speed + 0.1, 5)
     
        if pressed_keys[pg.K_DOWN]:
            self.speed = max(self.speed - 0.1, 0)
         
        if pressed_keys[pg.K_LEFT]:
            self.angle = self.angle - 5
        
        if pressed_keys[pg.K_RIGHT]:
            self.angle = self.angle + 5
        self.rotation()
        self.movement()

    def set_position(self, x = 160, y = 500):
        self.x, self.y = x, y
        self.rect.center = (x, y)

    def set_angle(self,angle=0):
        self.angle=angle
        self.rotation()

    def reset_speed(self):
        self.speed = 0

    def reset_angle(self):
        self.angle = 0
 
    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def check_rays(self, track, draw = False, max_length = 300):
        ray_angles = [-90,-60, -45, -25, -15, -7.5, 0, 7.5, 15, 25, 45, 60, 90]
        collisions = []
        rays = []
        for ray_angle in ray_angles:
            ray_result = self.check_ray(track, max_length, ray_angle, draw)
            intensity = 1 - ray_result[0] / max_length
            rays.append([ray_angle, intensity])     
            if draw:
                collisions.append([ray_result[1],ray_result[2]])
        return collisions

    def check_ray(self, track,  max_length, ray_angle, draw = False,):
        length = 0
        x,y = self.rect.center

        while length < max_length and not track.is_wall(x,y):
            x = int(self.rect.center[0] + math.sin(math.radians(self.angle + ray_angle)) * length)
            y = int(self.rect.center[1] - math.cos(math.radians(self.angle + ray_angle)) * length)
            length += 1

        if draw:
            return length, x, y
        return length

