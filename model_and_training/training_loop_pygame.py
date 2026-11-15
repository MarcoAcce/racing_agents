from symple_pygame import TrainingGame

environment = TrainingGame(track="oval", n_cars = 8, render = False)
max_steps = 1000

environment.reset()
observations = environment.observations
for step in range(max_steps):
    #actions = ...
    environment.step(actions)
    new_observations = environment.observations
    for i in range(len(environment.players)):
        # consider rewards and observations
        pass
    #learn
    observations = new_observations
    