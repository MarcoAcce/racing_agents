import pygame
import math
from pygame import locals as pg

ARROW = [(-20, -5), (5, -5), (5, -12), (20, 0), (5, 12), (5, 5), (-20, 5)]  # points right, centered on (0, 0)
black = pygame.Color(0, 0, 0)   
pygame.font.init()
myfont = pygame.font.SysFont("monospace", 16)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        image = pygame.image.load('Car.png')
        self.image = pygame.transform.scale(image, (60, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
        self.speed = 0
        self.speed_x, self.speed_y = 0, 0
        self.angle = 0

    def movement(self):
        if self.angle >= 360:
            self.angle = self.angle - 360
        if self.angle < 0:
            self.angle = 360 + self.angle
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
            self.angle = self.angle - 10
        
        if pressed_keys[pg.K_RIGHT]:
            self.angle = self.angle + 10
        self.movement()

    def reset_position(self):
        self.rect.center = (160, 520)

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

    def draw_arrow(self, surf, color):
        if self.speed == 0:
            return
        angle_rad = math.radians(self.angle)
        direction = math.atan2(-math.cos(angle_rad) * self.speed, math.sin(angle_rad) * self.speed)
        c, s = math.cos(direction), math.sin(direction)
        points = [(self.rect.centerx + x * c - y * s, self.rect.centery + x * s + y * c) for x, y in ARROW]
        pygame.draw.polygon(surf, color, points)
