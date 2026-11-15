from .game import Game
from .ai_car import AICar

class TrainingGame(Game):
    def __init__(self, track = "stadium", n_cars: int = 2, render: bool = False):
        super().__init__()
        self.initialize_track(track)
        for i in range(n_cars):
            self.register_player(human=False)
        self.render_enabled = render
        self.observations = []

    def reset(self):
        self.observations = []
        for player in self.players:
            player.reset_speed()
            player.reset_angle()
            player.set_position(*self.track.get_starting_position())
            player.set_angle(self.track.get_starting_angle())
            self.track.reset_player_state(player.id)
            player.check_rays(self.track, max_length=300)
            self.observations.append(player.get_observations())

    def step(self, actions):
        self.observations = []
        for player, action in zip(self.players, actions):
            player.nex_action = action
            player.update()
            self.track.check_position(player.id, player.mask, player.rect.topleft)
            #handle_events
            player.check_rays(self.track, max_length=300)
            self.observations.append(player.get_observations())
