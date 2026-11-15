from simple_pygame import TrainingGame
import random

n_epochs = 3
steps_per_epoch = 500

environment = TrainingGame(n_cars = 8, render = True)

for epoch in range(n_epochs):
    if environment.track_name == "oval": 
        environment.track_name = "stadium"
    else: 
        environment.track_name = "oval"
    environment.reset()
    for step in range(steps_per_epoch):
        observations = environment.observations
        actions = [ random.randrange(9) for _ in environment.players]
        environment.step(actions)
        rewards = [environment.rewards[player_id] 
            for player_id in sorted(environment.rewards.keys(), reverse=False)
        ]
        new_observations = environment.observations
        for i in range(len(environment.players)):
            reward = rewards[i]
            dones = environment.dones
            # consider done, rewards and observations
            new_action = random.randrange(9)
            actions.append(new_action)
        
        observations = new_observations
    #learn