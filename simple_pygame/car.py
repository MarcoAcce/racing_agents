import pygame
import math
import random
from pygame import locals as pg
from pathlib import Path

ASSETS = Path(__file__).parent
CAR_SPRITES = ASSETS / "cars"

def random_car_sprite():
    return random.choice(sorted(CAR_SPRITES.glob("*.png")))

class Car(pygame.sprite.Sprite):
    top_speed:int = 15

    def __init__(self, in_id: int = -1):
        super().__init__()
        self.base_image = pygame.image.load(random_car_sprite())
        self.set_scale(1)
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
        if accelerate: self.speed = min(
            self.speed + 0.1 * self.scale, 
            Car.top_speed * self.scale
        )
        if brake: self.speed = max(self.speed - 0.4 * self.scale, 0)
        if left: self.angle = self.angle - 5
        if right: self.angle = self.angle + 5

    def set_position(self, x = 160, y = 500):
        self.x, self.y = x, y
        self.rect.center = (x, y)

    def set_scale(self, scale = 1):
        """Resizes the car to the map's scale. Speeds and sensors scale with it."""
        self.scale = scale
        self.original_image = pygame.transform.smoothscale(
            self.base_image, (round(60 * scale), round(100 * scale))
        )

    def set_angle(self,angle=0):
        self.angle=angle
        self.rotation()

    def reset_speed(self):
        self.speed = 0

    def reset_angle(self):
        self.angle = 0
 
    def draw(self, surface):
        surface.blit(self.image, self.rect)


