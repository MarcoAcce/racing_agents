from .game import Game
from .map import Map

while True:
    map_choice = input(f"Choose a Map ({', '.join(Map.maps)}):")
    if map_choice in Map.maps:
        break
    print("wrong input")
game = Game()
game.initialize_track(map_choice)
game.register_player(human=True)
game.start()