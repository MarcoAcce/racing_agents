import sys
import pygame
import math
from pygame import locals as pg
from player import Player

pygame.init()

window_width = 1200
window_height = 800

display = pygame.display.set_mode((window_width, 
                                        window_height))

pygame.display.set_caption("racing game")

FPS = pygame.time.Clock()

white = pygame.Color(255, 255, 255)
grey = pygame.Color(128, 128, 128)  
red = pygame.Color(255, 0, 0)      

display.fill(white)
walls = display.get_rect().inflate(-10, -10)

if __name__ == "__main__":
    P1 = Player()
    while True:
        for event in pygame.event.get():
            if event.type == pg.QUIT:
                pygame.quit()
                sys.exit()
        display.fill(grey)
        pygame.draw.rect(display, red, walls, 2)
        P1.update()
        if not walls.contains(P1.rect):
            print("hit the wall")
            P1.reset_speed()
            P1.reset_angle()
            P1.reset_position()
        P1.draw(display)
        pygame.display.update()
        FPS.tick(60)