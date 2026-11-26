import sys
import pygame
from pygame import locals as pg
from .game import window_width, window_height
from .map import Map
from .colors import grey, red, white

class TrackSelection():
    controls = [
        "UP to accelerate, DOWN to brake, LEFT and RIGHT to steer",
        "Choose the track with UP and DOWN, start with ENTER",
    ]

    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption("racing game")
        self.font = pygame.font.Font(None, 80)
        self.small_font = pygame.font.Font(None, 40)
        self.track_names = list(Map.maps)
        self.selected = 0

    def choose(self):
        while True:
            self.draw()
            event = pygame.event.wait()
            if event.type == pg.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.selected = (self.selected - 1) % len(self.track_names)
                if event.key == pg.K_DOWN:
                    self.selected = (self.selected + 1) % len(self.track_names)
                if event.key == pg.K_RETURN:
                    return self.track_names[self.selected]

    def draw(self):
        self.display.fill(grey)
        center_x = window_width / 2
        title = self.font.render("Choose a track", True, white)
        self.display.blit(title, title.get_rect(center=(center_x, 150)))
        for i, name in enumerate(self.track_names):
            text = self.font.render(name, True, red if i == self.selected else white)
            self.display.blit(text, text.get_rect(center=(center_x, 300 + i * 90)))
        for i, line in enumerate(self.controls):
            text = self.small_font.render(line, True, white)
            self.display.blit(text, text.get_rect(center=(center_x, 900 + i * 50)))
        pygame.display.update()
