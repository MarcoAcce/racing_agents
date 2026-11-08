import pygame
import math
from pygame import locals as pg


class Car(pygame.sprite.Sprite):
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
        self.apply_controls(pressed_keys[pg.K_UP], pressed_keys[pg.K_DOWN], 
                            pressed_keys[pg.K_LEFT], pressed_keys[pg.K_RIGHT])
        self.rotation()
        self.movement()

    def apply_controls(self, accelerate = False, brake = False, left = False, right = False):
        if accelerate: self.speed = min(self.speed + 0.1, 5)
        if brake: self.speed = max(self.speed - 0.1, 0)
        if left: self.angle = self.angle - 5
        if right: self.angle = self.angle + 5

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


