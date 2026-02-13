from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Character import Character
    from Item import Item, ModifierType

class CharacterDecorator(ABC):
    def __init__(self, character: "Character"):
        self._character = character
    
    @abstractmethod
    def getStat(self, stat_name: str):
        pass


class BaseCharacterWrapper(CharacterDecorator):
    def getStat(self, stat_name: str):
        return getattr(self._character, stat_name, 0)


class StatModifierDecorator(CharacterDecorator):
    def __init__(self, character: "Character", item: "Item"):
        super().__init__(character)
        self.item = item
        self._base_decorator = None
    
    def getStat(self, stat_name: str):
        base_value = getattr(self._character, stat_name, 0)
        
        if stat_name not in self.item.affected_stats:
            return base_value
        
        from Item import ModifierType
        if self.item.modifier_type == ModifierType.ADD:
            return base_value + self.item.value
        elif self.item.modifier_type == ModifierType.PERCENTAGE:
            return base_value + int(base_value * (self.item.value / 100))
        
        return base_value


class StatCalculator:
    @staticmethod
    def calculateStat(character: "Character", stat_name: str) -> int:
        if not hasattr(character, 'inventory'):
            return getattr(character, stat_name, 0)
        
        inventory = character.inventory
        base_value = getattr(character, stat_name, 0)
        total_modifier = 0
        percentage_modifier = 0
        
        if inventory.equipped_weapon and stat_name in inventory.equipped_weapon.affected_stats:
            from Item import ModifierType
            if inventory.equipped_weapon.modifier_type == ModifierType.ADD:
                total_modifier += inventory.equipped_weapon.value
            else:
                percentage_modifier += inventory.equipped_weapon.value
        
        if inventory.equipped_armor and stat_name in inventory.equipped_armor.affected_stats:
            from Item import ModifierType
            if inventory.equipped_armor.modifier_type == ModifierType.ADD:
                total_modifier += inventory.equipped_armor.value
            else:
                percentage_modifier += inventory.equipped_armor.value
        
        final_value = base_value + total_modifier
        if percentage_modifier > 0:
            final_value += int(base_value * (percentage_modifier / 100))
        
        return final_value
    
    @staticmethod
    def getAllStats(character: "Character") -> dict:
        stats = {}
        stat_names = ['hp', 'hpMax', 'strength', 'defense', 'intelligence', 'agility', 'critChance']
        
        for stat_name in stat_names:
            stats[stat_name] = StatCalculator.calculateStat(character, stat_name)
        
        return stats
    
    @staticmethod
    def displayStats(character: "Character"):        
        print(f"\nStats of {character.name} (Level {character.level})")
        print("=" * 50)
        
        stat_names = {
            'hp': 'Health Points',
            'hpMax': 'Max HP',
            'strength': 'Strength',
            'defense': 'Defense',
            'intelligence': 'Intelligence',
            'agility': 'Agility',
            'critChance': 'Critical Chance'
        }
        
        for stat_key, stat_label in stat_names.items():
            if stat_key == 'hp':
                continue  # On affiche HP avec hpMax
            
            base_value = getattr(character, stat_key, 0)
            modified_value = StatCalculator.calculateStat(character, stat_key)
            
            if stat_key == 'hpMax':
                current_hp = character.hp
                max_hp = modified_value
                bonus = modified_value - base_value
                if bonus > 0:
                    print(f"  {stat_label:.<20} {current_hp}/{max_hp} (+{bonus})")
                else:
                    print(f"  {stat_label:.<20} {current_hp}/{max_hp}")
            else:
                if modified_value != base_value:
                    bonus = modified_value - base_value
                    print(f"  {stat_label:.<20} {modified_value} (+{bonus})")
                else:
                    print(f"  {stat_label:.<20} {modified_value}")
        
        print("=" * 50)
        
        if hasattr(character, 'inventory'):
            inventory = character.inventory
            print("\nEquipment:")
            if inventory.equipped_weapon:
                print(f"  Weapon: {inventory.equipped_weapon.getDescription()}")
            else:
                print(f"  Weapon: None")
            
            if inventory.equipped_armor:
                print(f"  Armor: {inventory.equipped_armor.getDescription()}")
            else:
                print(f"  Armor: None")
            print()
