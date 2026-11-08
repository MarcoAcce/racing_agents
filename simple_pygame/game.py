import sys
import pygame
from pygame import locals as pg
from car import Car
from ai_player import AICar
from map import Map, COLLISION, CHECKPOINT, FINISH, BACKWARDS


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

    P1 = AICar(1)
    track = Map(display, choice)
    track.register_player(P1)
    P1.set_position(*track.get_starting_position())
    P1.set_angle(track.get_starting_angle())

    while True:
        display.fill(grey)
        track.draw(display,red,2)
        track.check_position(P1.id, P1.mask, P1.rect.topleft)
        for event in pygame.event.get():
            if event.type == pg.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == COLLISION:
                print("hit the wall")
                P1.reset_speed()
                P1.reset_angle()
                P1.set_position(*track.get_starting_position())
                P1.set_angle(track.get_starting_angle())
                track.reset_player_state(P1.id)
                P1.check_rays(track, False, 300)
            if event.type == CHECKPOINT:
                print(f"checkpoint {event.index +1}!")
            if event.type == BACKWARDS:
                print(f"going backwards through {event.index +1}!")
            if event.type == FINISH:
                print("finish!")
                P1.reset_speed()
        P1.update()
        P1.draw(display)

        ray_collisions = P1.check_rays(track, True, 300)
        for point in ray_collisions:
            pygame.draw.line(display, white, P1.rect.center, point, 1)
            pygame.draw.circle(display, red, point, 3)
        pygame.display.update()
        FPS.tick(60)