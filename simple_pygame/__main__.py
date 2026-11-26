import queue
import threading
from pathlib import Path
import pygame
import torch
from model_and_training.sensor_brain_model import SensorBrain
from .game import Game
from .track_selection import TrackSelection
from .ai_car import AICar
from .colors import white

WEIGHTS = Path(__file__).parent.parent / "model_and_training" / "sensor_brain_weights.pt"
COAST = 8  # coast, no turn

observations_queue = queue.Queue()  # main thread -> brain
actions_queue = queue.Queue()       # brain -> main thread

def brain_loop(brain):
    while True:
        observations = observations_queue.get()
        actions_queue.put(brain.decide(observations))

def get_action(observations):
    try:
        action = actions_queue.get_nowait()
    except queue.Empty:
        return COAST
    observations_queue.put(observations)  
    return action

map_choice = TrackSelection().choose()

brain = SensorBrain()
brain.load_state_dict(torch.load(WEIGHTS))
threading.Thread(target=brain_loop, args=(brain,), daemon=True).start()
actions_queue.put(COAST)  

game = Game()
game.initialize_track(map_choice)
game.register_player(human=True)
game.register_player(human=False)
game.get_action = get_action

font = pygame.font.Font(None, 40)
game.legend = pygame.Surface((140, 100), pygame.SRCALPHA)
for row, player in enumerate(game.players.values()):
    name = "AI" if isinstance(player, AICar) else "Player"
    game.legend.blit(pygame.transform.smoothscale(player.base_image, (24, 40)), (0, row * 60))
    game.legend.blit(font.render(name, True, white), (40, row * 60 + 8))

game.start()
