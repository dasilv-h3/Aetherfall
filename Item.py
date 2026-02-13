from enum import Enum
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Character import Character

class ItemType(Enum):
    WEAPON = "weapon"
    ARMOR = "armor"
    CONSUMABLE = "consumable"

class ModifierType(Enum):
    ADD = "add"
    PERCENTAGE = "percentage"

class Item:
    def __init__(self, name: str, item_type: ItemType, minimal_level: int, 
                 modifier_type: ModifierType, value: int, affected_stats: list, 
                 apparition_rate: int):
        self.name = name
        self.item_type = item_type
        self.minimal_level = minimal_level
        self.modifier_type = modifier_type
        self.value = value
        self.affected_stats = affected_stats
        self.apparition_rate = apparition_rate

    def canUse(self, character: "Character") -> bool:
        return character.level >= self.minimal_level

    def __str__(self):
        return f"{self.name} (Lvl {self.minimal_level})"

    def __repr__(self):
        return self.__str__()


class Weapon(Item):
    def __init__(self, name: str, minimal_level: int, modifier_type: ModifierType, 
                 value: int, affected_stats: list, apparition_rate: int):
        super().__init__(name, ItemType.WEAPON, minimal_level, modifier_type, 
                        value, affected_stats, apparition_rate)

    def getDescription(self) -> str:
        stats_desc = ", ".join([f"+{self.value} {stat}" for stat in self.affected_stats])
        return f"Weapon: {self.name} - {stats_desc}"


class Armor(Item):
    def __init__(self, name: str, minimal_level: int, modifier_type: ModifierType, 
                 value: int, affected_stats: list, apparition_rate: int):
        super().__init__(name, ItemType.ARMOR, minimal_level, modifier_type, 
                        value, affected_stats, apparition_rate)

    def getDescription(self) -> str:
        stats_desc = ", ".join([f"+{self.value} {stat}" for stat in self.affected_stats])
        return f"Armor: {self.name} - {stats_desc}"


class Consumable(Item):
    def __init__(self, name: str, minimal_level: int, modifier_type: ModifierType, 
                 value: int, affected_stats: list, apparition_rate: int):
        super().__init__(name, ItemType.CONSUMABLE, minimal_level, modifier_type, 
                        value, affected_stats, apparition_rate)
        self.is_used = False

    def getDescription(self) -> str:
        if "hp" in self.affected_stats:
            return f"Consumable: {self.name} - Restores {self.value} HP"
        elif "damage" in self.affected_stats:
            return f"Consumable: {self.name} - Deals {self.value} area damage"
        elif "status" in self.affected_stats:
            return f"Consumable: {self.name} - Removes status effects"
        else:
            modifier = f"+{self.value}%" if self.modifier_type == ModifierType.PERCENTAGE else f"+{self.value}"
            stats_desc = ", ".join([f"{modifier} {stat}" for stat in self.affected_stats])
            return f"{self.name} - {stats_desc}"

    def use(self, character: "Character"):
        if self.is_used:
            return False
        
        if not self.canUse(character):
            print(f"Level {self.minimal_level} required to use {self.name}")
            return False

        # Apply effects based on the type of consumable
        if "hp" in self.affected_stats:
            old_hp = character.hp
            character.hp = min(character.hp + self.value, character.hpMax)
            healed = character.hp - old_hp
            print(f"{character.name} uses {self.name} and restores {healed} HP! (HP: {character.hp}/{character.hpMax})")
        
        elif "damage" in self.affected_stats:
            print(f"{character.name} uses {self.name}! Deals {self.value} area damage!")
            return self.value  # Returns the damage to be used in combat
        
        elif "status" in self.affected_stats:
            print(f"{character.name} uses {self.name}! Removes status effects.")
        
        else:
            # For temporary buffs (strength potions, etc.)
            print(f"{character.name} uses {self.name}! Stats temporarily increased.")
        
        self.is_used = True
        return True
