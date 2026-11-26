import sys
import pygame
from pygame import locals as pg
import random
from .car import Car
from .ai_car import AICar
from .map import Map, COLLISION, CHECKPOINT, FINISH, BACKWARDS
from .colors import grey, red, white

window_width = 1920
window_height = 1080

class Game():
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((window_width, 
                                        window_height))
        pygame.display.set_caption("racing game")
        self.show_loading_screen()
        self.FPS = pygame.time.Clock()
        self.players = {}

    def show_loading_screen(self):
        """Shown until the first render, while the track loads"""
        self.display.fill(grey)
        font = pygame.font.Font(None, 200)
        text = font.render("LOADING", True, white)
        self.display.blit(text, text.get_rect(center=self.display.get_rect().center))
        pygame.display.update()

    def initialize_track(self, track_choice):
        self.track = Map(self.display, track_choice)

    def register_player(self, human = False):    
        if human:
            player = Car(len(self.players))
        else:
            player = AICar(len(self.players))
        self.players[player.id]=player
        self.track.register_player(player)
    
    def start(self):
        for player in self.players.values():
            self.reset_player(player.id)
        self.game_loop()
    
    def game_loop(self):
        while True:
            self.update()
            self.handle_events()
            self.render()
            self.FPS.tick(60)

    def update(self):
        for player in self.players.values():
            if isinstance(player, AICar):
                player.check_rays(self.track, 500)
                observations = player.get_observations()
                #determine action from observations
                player.nex_action = random.randrange(9)
            player.update()
            self.track.check_position(player.id, player.mask, player.rect.topleft)
    
    def render(self):
        self.display.fill(grey)
        self.track.draw(self.display, red, 3)
        for player in self.players.values():
            player.draw(self.display)
        pygame.display.update()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pg.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == COLLISION:
                print(f"Player {event.player_id} hit the wall")
                self.reset_player(event.player_id)
            if event.type == CHECKPOINT:
                print(f"Player {event.player_id}: checkpoint {event.index +1}!")
            if event.type == BACKWARDS:
                print(f"Player {event.player_id}: going backwards through {event.index +1}!")
            if event.type == FINISH:
                player = self.players[event.player_id]
                print(f"Player {event.player_id}: finished!")
                self.reset_player(event.player_id)

    def reset_player(self, player_id):
        player = self.players[player_id]
        player.reset_speed()
        player.set_scale(self.track.scale)
        player.set_position(*self.track.get_starting_position())
        player.set_angle(self.track.get_starting_angle())
        self.track.reset_player_state(player_id)

