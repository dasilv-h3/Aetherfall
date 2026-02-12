from Character import *
from EnemyFactory import *
from Game import Game
from ZoneState import ForestState, VillageState
from Utils import inputMenu 

def buildGame() -> Game:
    player = Warrior("Charlie")
    enemy_factory = EnemyFactory()

    village = VillageState()
    forest = ForestState(enemy_factory)

    village.connect("forest", forest)
    forest.connect("village", village)

    game = Game(character=player, enemy_factory=enemy_factory, starting_location=village)
    return game


def main():
    choice = inputMenu("Main Menu", ["Nouvelle partie", "Charger partie", "Quitter"])

    if choice == 1:
        random.seed() # Initialize random seed for the game
        game = buildGame()
        game.run()
    elif choice == 2:
        print("Load game feature not implemented yet.")
        exit(0)
    elif choice == 3:
        exit(0)
    return 0

if __name__ == "__main__":
    main()