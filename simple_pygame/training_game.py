import sys
import pygame
from pygame import locals as pg
from .map import COLLISION, CHECKPOINT, FINISH, BACKWARDS
from .game import Game
from .ai_car import AICar
from .colors import grey

class TrainingGame(Game):
    def __init__(self, 
            track_choice = "stadium",
            n_cars: int = 2, 
            render: bool = False):
        super().__init__()
        self.track_name = track_choice
        self.initialize_track(track_choice)
        self.tracks = {track_choice: self.track}
        for i in range(n_cars):
            self.register_player(human=False)
        self.render_enabled = render
        self.observations = {}
        self.rewards = {}
        self.dones = {}
        self.active_players = {}
        self.steps = 0

    def reset(self):
        self.observations = {}
        if self.track_name not in self.tracks:
            self.initialize_track(track_choice = self.track_name)
            self.tracks[self.track_name] = self.track
        self.track = self.tracks[self.track_name]
        self.active_players = self.players.copy()
        for player in self.players.values():
            self.reset_player(player.id)
            player.check_rays(self.track, max_length=500)
            self.observations[player.id] = player.get_observations()

    def show_text(self, lines):
        self.text_lines = lines
        if not self.render_enabled:
            self.display.fill(grey)
            self.draw_text()
            pygame.display.update()

    def step(self, actions):
        self.observations = {}
        self.dones = {}
        for player, action in zip(self.active_players.values(), actions):
            self.rewards[player.id] = 0
            player.nex_action = action
            player.update()
            self.track.check_position(player.id, player.mask, player.rect.topleft)
            self.handle_events()
            self.rewards[player.id] += self.still_penalty + self.speed_factor * player.speed / player.scale
            player.check_rays(self.track, max_length=500)
            self.observations[player.id] = player.get_observations()
        self.steps += 1
        if self.render_enabled:
            self.render(self.active_players)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pg.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == COLLISION:
                self.rewards[event.player_id] += self.crash_rw
                self.reset_player(event.player_id)        
                self.dones[event.player_id] = True
            if event.type == CHECKPOINT:
                self.rewards[event.player_id] += self.checkpoint_rw
            if event.type == BACKWARDS:
                self.rewards[event.player_id] += self.backwards_rw
            if event.type == FINISH:
                self.rewards[event.player_id] += self.finish_rw
                self.dones[event.player_id] = False

    def remove_player(self, player_id):
        self.active_players.pop(player_id, None)
        self.rewards.pop(player_id, None)
        self.dones.pop(player_id, None)

    def set_rewards(self, crash_rw = -50, checkpoint_rw = 3, 
    backwards_rw = -3, finish_rw = 50, still_penalty = -0.1, speed_factor = 0.01):
        self.crash_rw = crash_rw
        self.checkpoint_rw = checkpoint_rw
        self.backwards_rw = backwards_rw
        self.finish_rw = finish_rw
        self.still_penalty = still_penalty
        self.speed_factor = speed_factor
