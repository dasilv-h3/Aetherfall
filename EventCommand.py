from abc import ABC, abstractmethod
import random

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
    def __init__(self, loot_table = None, gold_range=(5, 20)):
        self.loot_table = loot_table or ["Potion", "Antidote", "Bombe"]
        self.gold_range = gold_range

    def execute(self, game) -> None:
        print("\n[Coffre] Vous trouvez un coffre !")
        loot = random.choice(self.loot_table)
        gold = random.randint(*self.gold_range)
        print(f"Vous obtenez : {loot} et {gold} pièces d'or !")

class CombatEvent(Event):
    def __init__(self, enemy):
        self.enemy = enemy

    def execute(self, game) -> None:
        print(f"\n[Combat] Un {self.enemy.name} niveau {self.enemy.level} apparaît !")