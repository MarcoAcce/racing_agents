import sys
import pygame
from pygame import locals as pg
from .map import COLLISION, CHECKPOINT, FINISH, BACKWARDS
from .game import Game
from .ai_car import AICar

class TrainingGame(Game):
    def __init__(self, 
            track = "stadium", 
            n_cars: int = 2, 
            render: bool = False):
        super().__init__()
        self.initialize_track(track)
        for i in range(n_cars):
            self.register_player(human=False)
        self.render_enabled = render
        self.observations = []
        self.rewards = {}
        self.dones = []
        self.steps = 0

    def reset(self):
        self.observations = []
        for player in self.players:
            self.reset_player(player.id)
            player.check_rays(self.track, max_length=300)
            self.observations.append(player.get_observations())

    def step(self, actions):
        self.observations = []
        self.dones = []
        for player, action in zip(self.players, actions):
            self.rewards[player.id] = 0
            player.nex_action = action
            player.update()
            self.track.check_position(player.id, player.mask, player.rect.topleft)
            self.handle_events()
            self.rewards[player.id] += -0.01 + 0.01 * player.speed
            player.check_rays(self.track, max_length=300)
            self.observations.append(player.get_observations())
        self.steps += 1
        if self.render_enabled:
            self.render()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pg.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == COLLISION:
                self.rewards[event.player_id] += -15
                self.reset_player(event.player_id)
                self.dones.append(event.player_id)
            if event.type == CHECKPOINT:
                self.rewards[event.player_id] += 2
            if event.type == BACKWARDS:
                self.rewards[event.player_id] += -3
            if event.type == FINISH:
                self.rewards[event.player_id] += 15
                self.reset_player(event.player_id)
                self.dones.append(event.player_id)