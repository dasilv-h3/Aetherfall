from entity.Character import *
from entity.EnemyFactory import *
from Game import Game
from zone.ZoneState import ForestState, VillageState
from Utils import inputMenu
from item.ItemFactory import ItemFactory
from SaveGame import SaveGame

def buildGame(character=None) -> Game:
    if character:
        player = character
    else:
        playerName = input("Enter your character's name: ")

        player_class_choice = inputMenu("Choose your class", ["Warrior", "Mage", "Rogue"])
        if player_class_choice == 1:
            player = Warrior(playerName)
        elif player_class_choice == 2:
            player = Mage(playerName)
        elif player_class_choice == 3:
            player = Thief(playerName)
        else:
            player = Warrior(playerName)  # Default to Warrior if invalid choice

    enemy_factory = EnemyFactory()
    item_factory = ItemFactory()
    
    # Ajoute quelques potions
    for _ in range(2):
        potion = item_factory.createConsumable("Potion de soin")
        if potion:
            player.inventory.addItem(potion)
    
    print(f"\nStarting stats:")
    player.displayStats()

    village = VillageState()
    forest = ForestState(enemy_factory)

    village.connect("forest", forest)
    forest.connect("village", village)

    game = Game(character=player, enemy_factory=enemy_factory, starting_location=village)
    return game


def main():
    while True:
        choice = inputMenu("Main Menu", ["Nouvelle partie", "Charger partie", "Quitter"])

        if choice == 1:
            random.seed()
            game = buildGame()
            game.run()
        elif choice == 2:
            save_manager = SaveGame()
            character = save_manager.load()
            if character:
                game = buildGame(character)
                game.run()
        elif choice == 3:
            exit(0)

if __name__ == "__main__":
    main()