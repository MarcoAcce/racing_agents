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
        self.text_lines = []
        self.font = pygame.font.Font(None, 40)
        self.legend = None  

    def show_loading_screen(self):
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
                player.nex_action = self.get_action(observations)
            player.update()
            self.track.check_position(player.id, player.mask, player.rect.topleft)

    def get_action(self, observations):
        """Action of an AI car for this tick, random unless replaced by a brain"""
        return random.randrange(9)

    def render(self, players_to_draw = None):
        self.draw_frame(players_to_draw)
        self.draw_text()
        if self.legend is not None:
            self.display.blit(self.legend, self.legend.get_rect(topright=(window_width - 20, 20)))
        pygame.display.update()

    def draw_frame(self, players_to_draw = None):
        if players_to_draw == None:
            players_to_draw = self.players
        self.display.fill(grey)
        self.track.draw(self.display, red, 3)
        for player in players_to_draw.values():
            player.draw(self.display)

    def draw_text(self):
        y = self.display.get_height() - 20
        for line in reversed(self.text_lines):
            text = self.font.render(line, True, white)
            y -= text.get_height()
            self.display.blit(text, (20, y))
            y -= 5

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pg.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == COLLISION:
                name = "AI" if isinstance(self.players[event.player_id], AICar) else "Player"
                self.text_lines.append(f"{name} hit the wall")
                self.text_lines = self.text_lines[-3:]  # only the last 3 messages
                self.reset_player(event.player_id)
            if event.type == CHECKPOINT:
                pass
            if event.type == BACKWARDS:
                pass
            if event.type == FINISH:
                name = "AI" if isinstance(self.players[event.player_id], AICar) else "Player"
                self.text_lines.append(f"{name} finished a lap")
                self.text_lines = self.text_lines[-3:]  # only the last 3 messages

    def reset_player(self, player_id):
        player = self.players[player_id]
        player.reset_speed()
        player.set_scale(self.track.scale)
        player.set_position(*self.track.get_starting_position())
        player.set_angle(self.track.get_starting_angle())
        self.track.reset_player_state(player_id)

