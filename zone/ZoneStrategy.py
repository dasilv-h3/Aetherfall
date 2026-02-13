from abc import ABC, abstractmethod
import random
from typing import Optional
from entity.EnemyFactory import EnemyFactory
from EventCommand import ChestEvent, CombatEvent, DialogueEvent, Event, ShopEvent
from Game import *

class ZoneStrategy(ABC):
    @abstractmethod
    def nextEvent(self, game: "Game") -> Optional[Event]:
        pass

class VillageStrategy(ZoneStrategy):
    def nextEvent(self, game: "Game") -> Optional[Event]:
        return None

    def talkToVillagers(self):
        return DialogueEvent("Villager", "Welcome to our village, traveler! Feel free to rest and talk to us.")
    
    def merchantEvent(self):
        return ShopEvent()

class ForestStrategy(ZoneStrategy):
    def __init__(self, enemy_factory : EnemyFactory):
        self.enemy_factory = enemy_factory
        self.resetRun()
    
    def resetRun(self):
        self.remaining_combats = random.randint(2, 4)
        self.remaining_chests = random.randint(1, 3)
        self.key_can_drop = True
    
    def nextEvent(self, game: "Game") -> Optional[Event]:
        if self.remaining_combats <= 0 and self.remaining_chests <= 0:
            print("You have cleared the forest! Time to move on to the next zone.")            
            return None
        
        choices = []
        if self.remaining_combats > 0:
            choices.extend(["combat"] * self.remaining_combats)
        if self.remaining_chests > 0:
            choices.extend(["chest"] * self.remaining_chests)
    
        kind = random.choice(choices)
        if kind == "combat":
            self.remaining_combats -= 1
            enemy_type = random.choice(["Wolf", "Bandit", "Skeleton"])
            enemy_level = random.randint(1, 5)
            enemy = self.enemy_factory.create_enemy(enemy_type, enemy_level)
            return CombatEvent(enemy)
        else:
            self.remaining_chests -= 1
            if self.key_can_drop and random.random() < 0.1: # TODO : Adjust drop chance as needed and player inventory conditions
                self.key_can_drop = False
                return ChestEvent(loot_table=["Dungeon Key"])

            return ChestEvent()