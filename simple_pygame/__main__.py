from .game import Game

while True:
    map_choice = input("Choose a Map (oval, stadium):")
    if map_choice in ("oval","stadium"):
        break
    print("wrong input")
game = Game()
game.initialize_track(map_choice)
game.register_player(human=True)
game.start()