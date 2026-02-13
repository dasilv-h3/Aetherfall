import json
import random
import os
from typing import Optional, List
from Item import Item, Weapon, Armor, Consumable, ItemType, ModifierType

class ItemFactory:    
    def __init__(self, items_file: str = "items.json"):
        self.items_data = {}
        self.items_file = items_file
        self.loadItems()
    
    def loadItems(self):
        try:
            # Trouve le chemin absolu du fichier JSON
            if not os.path.isabs(self.items_file):
                script_dir = os.path.dirname(os.path.abspath(__file__))
                self.items_file = os.path.join(script_dir, self.items_file)
            
            with open(self.items_file, 'r', encoding='utf-8') as f:
                self.items_data = json.load(f)
            print(f"Items loaded from {self.items_file}")
        except FileNotFoundError:
            print(f"File {self.items_file} not found. Using default data.")
            self.items_data = {"weapons": [], "armors": [], "consumables": []}
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            self.items_data = {"weapons": [], "armors": [], "consumables": []}
    
    def createItemFromData(self, item_data: dict, item_type: str) -> Optional[Item]:
        try:
            name = item_data["name"]
            minimal_level = item_data["minimalLevel"]
            modifier_type = ModifierType(item_data["modifierType"])
            value = item_data["value"]
            affected_stats = item_data["affectedStats"]
            apparition_rate = item_data["apparitionRate"]
            
            if item_type == "weapon":
                return Weapon(name, minimal_level, modifier_type, value, affected_stats, apparition_rate)
            elif item_type == "armor":
                return Armor(name, minimal_level, modifier_type, value, affected_stats, apparition_rate)
            elif item_type == "consumable":
                return Consumable(name, minimal_level, modifier_type, value, affected_stats, apparition_rate)
            
        except KeyError as e:
            print(f"Missing data for item: {e}")
            return None
        except ValueError as e:
            print(f"Invalid value for item: {e}")
            return None
    
    def createWeapon(self, name: str) -> Optional[Weapon]:
        for weapon_data in self.items_data.get("weapons", []):
            if weapon_data["name"] == name:
                return self.createItemFromData(weapon_data, "weapon")
        print(f"Warning: Weapon '{name}' not found")
        return None
    
    def createArmor(self, name: str) -> Optional[Armor]:
        for armor_data in self.items_data.get("armors", []):
            if armor_data["name"] == name:
                return self.createItemFromData(armor_data, "armor")
        print(f"Warning: Armor '{name}' not found")
        return None
    
    def createConsumable(self, name: str) -> Optional[Consumable]:
        for consumable_data in self.items_data.get("consumables", []):
            if consumable_data["name"] == name:
                return self.createItemFromData(consumable_data, "consumable")
        print(f"Warning: Consumable '{name}' not found")
        return None
    
    def getRandomWeapon(self, max_level: int = 100) -> Optional[Weapon]:
        available_weapons = [
            w for w in self.items_data.get("weapons", [])
            if w["minimalLevel"] <= max_level
        ]
        
        if not available_weapons:
            return None

        weights = [w["apparitionRate"] for w in available_weapons]
        chosen_data = random.choices(available_weapons, weights=weights, k=1)[0]
        return self.createItemFromData(chosen_data, "weapon")
    
    def getRandomArmor(self, max_level: int = 100) -> Optional[Armor]:
        available_armors = [
            a for a in self.items_data.get("armors", [])
            if a["minimalLevel"] <= max_level
        ]
        
        if not available_armors:
            return None
        
        weights = [a["apparitionRate"] for a in available_armors]
        chosen_data = random.choices(available_armors, weights=weights, k=1)[0]
        return self.createItemFromData(chosen_data, "armor")
    
    def getRandomConsumable(self, max_level: int = 100) -> Optional[Consumable]:
        available_consumables = [
            c for c in self.items_data.get("consumables", [])
            if c["minimalLevel"] <= max_level
        ]
        
        if not available_consumables:
            return None
        
        weights = [c["apparitionRate"] for c in available_consumables]
        chosen_data = random.choices(available_consumables, weights=weights, k=1)[0]
        return self.createItemFromData(chosen_data, "consumable")
    
    def getRandomItem(self, max_level: int = 100) -> Optional[Item]:
        item_types = ["weapon", "armor", "consumable"]
        chosen_type = random.choice(item_types)
        
        if chosen_type == "weapon":
            return self.getRandomWeapon(max_level)
        elif chosen_type == "armor":
            return self.getRandomArmor(max_level)
        else:
            return self.getRandomConsumable(max_level)
    
    def getAllWeapons(self) -> List[Weapon]:
        weapons = []
        for weapon_data in self.items_data.get("weapons", []):
            weapon = self.createItemFromData(weapon_data, "weapon")
            if weapon:
                weapons.append(weapon)
        return weapons
    
    def getAllArmors(self) -> List[Armor]:
        armors = []
        for armor_data in self.items_data.get("armors", []):
            armor = self.createItemFromData(armor_data, "armor")
            if armor:
                armors.append(armor)
        return armors
    
    def getAllConsumables(self) -> List[Consumable]:
        consumables = []
        for consumable_data in self.items_data.get("consumables", []):
            consumable = self.createItemFromData(consumable_data, "consumable")
            if consumable:
                consumables.append(consumable)
        return consumables
    
    def display_catalog(self):
        print("\n" + "=" * 70)
        print("ITEMS CATALOG")
        print("=" * 70)
        
        print("\nWEAPONS:")
        print("-" * 70)
        weapons = self.getAllWeapons()
        for weapon in weapons:
            print(f"  {weapon.getDescription()} - Lvl {weapon.minimal_level} - Rarity: {weapon.apparition_rate}")
        
        print("\nARMORS:")
        print("-" * 70)
        armors = self.getAllArmors()
        for armor in armors:
            print(f"  {armor.getDescription()} - Lvl {armor.minimal_level} - Rarity: {armor.apparition_rate}")
        
        print("\nCONSUMABLES:")
        print("-" * 70)
        consumables = self.getAllConsumables()
        for consumable in consumables:
            print(f"  {consumable.getDescription()} - Lvl {consumable.minimal_level} - Rarity: {consumable.apparition_rate}")
        
        print("=" * 70 + "\n")
