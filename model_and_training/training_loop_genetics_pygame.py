from pathlib import Path
import torch
from torch.nn.utils import parameters_to_vector, vector_to_parameters
from simple_pygame import TrainingGame
from simple_pygame.map import Map
from .sensor_brain_model import SensorBrain

CHECKPOINTS_DIR = Path(__file__).parent / "checkpoints" / "genetics"

scores = {}
brains = {}
actions = {}

def get_models(n_models: int):
    """Loads the latest generation checkpoint and fills up with new models.
    Returns (models, next_generation, best score of the loaded generation)."""
    models, next_generation, best_score = [], 0, None
    files = sorted(CHECKPOINTS_DIR.glob("gen_*.pt"))
    if files:
        latest = files[-1]
        next_generation = int(latest.stem.split("_")[1]) + 1
        checkpoint = torch.load(latest)
        for state in checkpoint["models"][:n_models]:
            model = SensorBrain()
            model.load_state_dict(state)
            models.append(model)
        best_score = checkpoint["scores"][0]
        print(f"Loaded {latest.name}: {len(models)} models, best score {best_score:.1f}")
    else:
        print("No checkpoint found, starting with new models")
    while len(models) < n_models:
        models.append(SensorBrain())
    return models, next_generation, best_score

def save_models(brains, scores, generation):
    """Saves generation's checkpoint (models and scores, best first).
    The best model is saved in best.pt and overwritten every generation."""
    ranked_ids = sorted(scores, key=scores.get, reverse=True) # player ids best first
    CHECKPOINTS_DIR.mkdir(parents=True, exist_ok=True)
    path = CHECKPOINTS_DIR / f"gen_{generation:04d}.pt"
    torch.save({
        "scores": [scores[pid] for pid in ranked_ids],
        "models": [brains[pid].state_dict() for pid in ranked_ids],
    }, path)
    torch.save(brains[ranked_ids[0]].state_dict(), CHECKPOINTS_DIR / "best.pt")

@torch.no_grad()
def mutate(parent_models, mutation_rate = 0.1, mutation_size = 0.2):
    weights = torch.stack([parameters_to_vector(model.parameters()) for model in parent_models])
    chance, change = torch.rand(2, *weights.shape) #two random numbers per model weight
    mask = chance < mutation_rate
    weights = weights + mask * (2 * change - 1) * mutation_size
    children_models = []
    for row in weights:
        child = SensorBrain()
        vector_to_parameters(row, child.parameters())
        children_models.append(child)
    return children_models

def reset_env(environment, track_name):
    """Switches the environment to the given map and resets it."""
    environment.track_name = track_name
    environment.reset()
    
def single_game(environment, steps):
    for step in range(steps):
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
        if list(dones.values()).count(True) == len(dones):
            break

if __name__ == "__main__":
    while True:
        answer = input("Number of cars, must be even (default 20):") or "20"
        if answer.isdigit() and int(answer) > 0 and int(answer) % 2 == 0:
            break
        print("wrong input")
    n_cars = int(answer)

    while True:
        answer = input("Initial steps per epoch (default 400):") or "400"
        if answer.isdigit() and int(answer) > 0:
            break
        print("wrong input")
    steps_per_epoch = int(answer)

    while True:
        answer = input("Increase the steps every epoch? y/n (default n):") or "n"
        if answer in ("y", "n"):
            break
        print("wrong input")
    increase_steps = answer == "y"

    while True:
        answer = input("Draw? y/n (default y):") or "y"
        if answer in ("y", "n"):
            break
        print("wrong input")
    draw = answer == "y"

    while True:
        answer = input("Number of epochs (default 10):") or "10"
        if answer.isdigit() and int(answer) > 0:
            break
        print("wrong input")
    n_epochs = int(answer)

    environment = TrainingGame(n_cars = n_cars, render = draw)
    models, generation, previous_best = get_models(n_cars)
    for player, i in zip(environment.players.values(), range(n_cars)):
        brains[player.id] = models[i]
    for epoch in range(n_epochs):
        scores = {pid : 0  for pid in environment.players}
        current_best = None
        for track_name in Map.maps:
            reset_env(environment, track_name)
            environment.show_text([
                f"epoch: {epoch + 1}/{n_epochs}",
                f"track: {track_name}",
                f"current best: {'-' if current_best is None else round(current_best, 1)}",
                f"previous epoch best: {'-' if previous_best is None else round(previous_best, 1)}",
            ])
            environment.set_rewards(
                crash_rw = -steps_per_epoch/10,
                checkpoint_rw = 5,
                backwards_rw = -5,
                finish_rw = steps_per_epoch/5,
                still_penalty = -0.1,
                speed_factor = 0.02
            )
            single_game(environment, steps_per_epoch)
            current_best = max(scores.values())

        save_models(brains, scores, generation)
        previous_best = max(scores.values())
        ranked_model_ids = sorted(scores, key=scores.get, reverse=True) #player ids best first
        parents = [brains[pid] for pid in ranked_model_ids[: int(n_cars/2) ]]
        models = parents + mutate(parents)
        brains = {pid: models[i] for i, pid in enumerate(environment.players)}
        generation += 1
        if increase_steps:
            steps_per_epoch += 10
