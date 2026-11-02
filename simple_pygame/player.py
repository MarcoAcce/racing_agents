import pygame
import math
from pygame import locals as pg


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        image = pygame.image.load('Car.png')
        self.original_image = pygame.transform.scale(image, (60, 100))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 0
        self.speed_x, self.speed_y = 0, 0
        self.angle = 0

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
        self.rect.move_ip(hor,ver)

    def update(self):
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pg.K_UP]:
            self.speed = self.speed + 1
     
        if pressed_keys[pg.K_DOWN]:
            self.speed = max(self.speed - 1,0)
         
        if pressed_keys[pg.K_LEFT]:
            self.angle = self.angle - 5
        
        if pressed_keys[pg.K_RIGHT]:
            self.angle = self.angle + 5
        self.rotation()
        self.movement()

    def set_position(self, x = 160, y = 500):
        self.rect.center = (x, y)

    def set_angle(self,angle=0):
        self.angle=angle
        self.rotation

    def reset_speed(self):
        self.speed = 0

    def reset_angle(self):
        self.angle = 0
 
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        speed_text = myfont.render(f"speed {self.speed}", 1, (0,0,0))
        surface.blit(speed_text, (5, 10))     
        angle_text = myfont.render(f"angle {self.angle}", 1, (0,0,0))
        surface.blit(angle_text, (5, 30))     
        self.draw_arrow(surface, black)

