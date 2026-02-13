from abc import ABC, abstractmethod
import random
from CombatStrategy import CombatSystem
from item.ItemFactory import ItemFactory

class Event(ABC):
    @abstractmethod
    def execute(self, game) -> None:
        pass

class DialogueEvent(Event):
    def __init__(self, from_character: str, dialogue: str):
        self.from_character = from_character
        self.text = dialogue or "..."

    def execute(self, game) -> None:
        print(f"\n{self.from_character} : \"{self.text}\"")

class ShopEvent(Event):
    def __init__(self):
        self.shop_items = ["Potion", "Sword", "Shield"]

    def execute(self, game) -> None:
        print("Welcome to the shop! Here are the items available for purchase:")

class ChestEvent(Event):
    def __init__(self, loot_table: str = None, gold_range=(5, 20)):
        self.loot_table = loot_table
        self.gold_range = gold_range

    def execute(self, game) -> None:
        gold = random.randint(*self.gold_range)
        loot = None
        item_factory = ItemFactory()
        
        if self.loot_table:
            loot = item_factory.createConsumable(self.loot_table)
        else:
            chestType = random.choice(["weapon", "armor", "consumable"])
            if chestType == "weapon":
                loot = item_factory.getRandomWeapon(max_level=game.character.level)
            elif chestType == "armor":
                loot = item_factory.getRandomArmor(max_level=game.character.level)
            else:
                loot = item_factory.getRandomConsumable(max_level=game.character.level)
        
        if loot:
            game.character.inventory.addItem(loot)
            print(f"Vous obtenez : {loot.name} et {gold} pièces d'or !")
        else:
            print(f"Vous obtenez {gold} pièces d'or !")

class CombatEvent(Event):
    def __init__(self, enemy):
        self.enemy = enemy

    def execute(self, game) -> None:
        combat = CombatSystem(game.character, self.enemy)
        victory = combat.start_combat()
        
        if not victory:
            print("\nYou must return to the village to heal...")
            # The player is teleported to the village
            if hasattr(game.location, 'connections') and 'village' in game.location.connections:
                game.location = game.location.connections['village']
                game.character.hp = game.character.hpMax  # Heals the player at the village
                print("You wake up in the village, fully healed.")
