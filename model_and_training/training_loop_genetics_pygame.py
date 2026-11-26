from pathlib import Path
import torch
from simple_pygame import TrainingGame
from simple_pygame.map import Map
from .sensor_brain_model import SensorBrain

CHECKPOINTS_DIR = Path(__file__).parent / "checkpoints" / "genetics"

n_epochs = 15
steps_per_epoch = 100
n_cars = 20

scores = {}
brains = {}
actions = {}

def get_models(n_models: int):
    """Loads the latest generation checkpoint and fills up with new models.
    Returns (models, next_generation)."""
    models, next_generation = [], 0
    files = sorted(CHECKPOINTS_DIR.glob("gen_*.pt"))
    if files:
        latest = files[-1]
        next_generation = int(latest.stem.split("_")[1]) + 1 
        for state in torch.load(latest)[:n_models]:
            model = SensorBrain()
            model.load_state_dict(state)
            models.append(model)
    while len(models) < n_models:
        models.append(SensorBrain())
    return models, next_generation

def save_models(models, scores, generation):
    """Saves generation's checkpoint, best model first."""
    ranked = sorted(zip(scores, models), key=lambda pair: pair[0], reverse=True)
    CHECKPOINTS_DIR.mkdir(parents=True, exist_ok=True)
    path = CHECKPOINTS_DIR / f"gen_{generation:04d}.pt"
    torch.save([model.state_dict() for _, model in ranked], path)

def reset_env(environment):
    """Switches the environment to the next map and resets it."""
    map_names = list(Map.maps)
    current = map_names.index(environment.track_name)
    environment.track_name = map_names[(current + 1) % len(map_names)]
    environment.reset()
    

def single_game(environment):
    for step in range(steps_per_epoch):
        observations = environment.observations
        actions = [ brains[player.id].decide(observations[player.id]) 
            for player in environment.active_players.values()
        ]
        environment.step(actions)
        rewards = environment.rewards
        new_observations = environment.observations
        dones = environment.dones
        for player in list(environment.active_players.values()):
            reward = rewards[player.id]
            scores[player.id] += reward
            if dones[player.id]:
                environment.remove_player(player.id)
        observations = new_observations

if __name__ == "__main__":
    environment = TrainingGame(n_cars = n_cars, render = True)
    models, generation = get_models(n_cars)   
    for player, i in zip(environment.players.values(), range(n_cars)):
        brains[player.id] = models[i]
    for epoch in range(n_epochs):
        scores = {pid : 0  for pid in environment.players}
        for _ in range(len(Map.maps)):
            reset_env(environment)
            environment.set_rewards(
                crash_rw = -steps_per_epoch * 0.3, 
                checkpoint_rw = 3, 
                backwards_rw = -3, 
                finish_rw = steps_per_epoch * 0.1,
                still_penalty = -0.1,
                speed_factor = 0.02
            )
            single_game(environment)
        #keep only the 10 best models, kepts as is
        #random mutations to the 10 best models to have a new set of 20
        #mutations and new models
        save_models(models, [scores[pid] for pid in environment.players], generation)
        generation += 1
        steps_per_epoch += 100
