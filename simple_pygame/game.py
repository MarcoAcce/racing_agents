import sys
import math
import pygame
from pygame import locals as pg
from player import Player
from map import Map, EmptyMap

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

# black = pygame.Color(0, 0, 0)   
# pygame.font.init()
# myfont = pygame.font.SysFont("monospace", 16)

if __name__ == "__main__":
    while True:
        choice = input("Choose a Map (oval, stadium):")
        if choice in ("oval","stadium"):
            break
        print("wrong input")

    P1 = Player()
    track = Map(display, choice)
    P1.set_position(*track.get_starting_position())
    P1.set_angle(track.get_starting_angle())
    while True:
        for event in pygame.event.get():
            if event.type == pg.QUIT:
                pygame.quit()
                sys.exit()
        display.fill(grey)
        track.draw(display,red,2)
        P1.update()
        if track.check_collision(P1):
            print("hit the wall")
            P1.reset_speed()
            P1.reset_angle()
            P1.set_position(*track.get_starting_position())
            P1.set_angle(track.get_starting_angle())
        P1.draw(display)
        pygame.display.update()
        FPS.tick(60)