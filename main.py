from entity.Character import *
from entity.EnemyFactory import *
from Game import Game
from zone.ZoneState import ForestState, VillageState
from Utils import inputMenu
from item.ItemFactory import ItemFactory

def buildGame() -> Game:
    playerName = input("Enter your character's name: ")
    player = Warrior(playerName)
    enemy_factory = EnemyFactory()
    
    # Initialise l'ItemFactory
    item_factory = ItemFactory()
    
    # Ajoute quelques potions
    for _ in range(3):
        potion = item_factory.createConsumable("Potion de soin")
        if potion:
            player.inventory.addItem(potion)

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