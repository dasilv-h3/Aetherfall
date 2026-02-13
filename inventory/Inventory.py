from typing import Optional, List
from item.Item import Item, Weapon, Armor, Consumable, ItemType

class Inventory:   
    MAX_SLOTS = 10
    
    def __init__(self):
        self.items: List[Item] = []
        self.equipped_weapon: Optional[Weapon] = None
        self.equipped_armor: Optional[Armor] = None
    
    def isFull(self) -> bool:
        return len(self.items) >= self.MAX_SLOTS
    
    def getAvailableSlots(self) -> int:
        return self.MAX_SLOTS - len(self.items)
    
    def addItem(self, item: Item) -> bool:
        if self.isFull():
            print(f"Inventory full ! {item.name} cannot be added.")
            return False
        
        self.items.append(item)
        print(f"{item.name} added to inventory ({len(self.items)}/{self.MAX_SLOTS})")
        return True
    
    def removeItem(self, item: Item) -> bool:
        if item in self.items:
            self.items.remove(item)
            print(f"{item.name} removed from inventory")
            return True
        return False
    
    def equipWeapon(self, weapon: Weapon, character) -> bool:
        if weapon not in self.items:
            print(f"{weapon.name} is not in the inventory")
            return False
        
        if not weapon.canUse(character):
            print(f"Level {weapon.minimal_level} required to equip {weapon.name}")
            return False
        
        # Unequip current weapon if any
        if self.equipped_weapon:
            print(f"{self.equipped_weapon.name} unequipped")
        
        self.equipped_weapon = weapon
        print(f"{weapon.name} equipped!")
        return True
    
    def equipArmor(self, armor: Armor, character) -> bool:
        if armor not in self.items:
            print(f"{armor.name} is not in the inventory")
            return False
        
        if not armor.canUse(character):
            print(f"Level {armor.minimal_level} required to equip {armor.name}")
            return False
        
        # Unequip current armor if any
        if self.equipped_armor:
            print(f"{self.equipped_armor.name} unequipped")
        
        self.equipped_armor = armor
        print(f"{armor.name} equipped!")
        return True
    
    def unequipWeapon(self) -> bool:
        if not self.equipped_weapon:
            print("No weapon equipped")
            return False
        
        print(f"{self.equipped_weapon.name} unequipped")
        self.equipped_weapon = None
        return True
    
    def unequipArmor(self) -> bool:
        if not self.equipped_armor:
            print("No armor equipped")
            return False
        
        print(f"{self.equipped_armor.name} unequipped")
        self.equipped_armor = None
        return True
    
    def useConsumable(self, consumable: Consumable, character) -> bool:
        if consumable not in self.items:
            print(f"{consumable.name} is not in the inventory")
            return False
        
        # Use the consumable
        result = consumable.use(character)
        
        # If used successfully, remove it from the inventory
        if result or consumable.is_used:
            self.removeItem(consumable)
        
        return result
    
    def getItemsByType(self, item_type: ItemType) -> List[Item]:
        return [item for item in self.items if item.item_type == item_type]
    
    def getWeapons(self) -> List[Weapon]:
        return [item for item in self.items if isinstance(item, Weapon)]
    
    def getArmors(self) -> List[Armor]:
        return [item for item in self.items if isinstance(item, Armor)]
    
    def getConsumables(self) -> List[Consumable]:
        return [item for item in self.items if isinstance(item, Consumable)]
    
    def display(self):
        print("\n" + "=" * 60)
        print(f"INVENTORY ({len(self.items)}/{self.MAX_SLOTS} slots)")
        print("=" * 60)
        
        # Display equipment
        print("\nCURRENT EQUIPMENT:")
        print("-" * 60)
        if self.equipped_weapon:
            print(f"  Weapon    : {self.equipped_weapon.getDescription()}")
        else:
            print(f"  Weapon    : None")
        
        if self.equipped_armor:
            print(f"  Armor  : {self.equipped_armor.getDescription()}")
        else:
            print(f"  Armor  : None")
        
        # Display weapons
        weapons = self.getWeapons()
        if weapons:
            print(f"\nWEAPONS ({len(weapons)}):")
            print("-" * 60)
            for i, weapon in enumerate(weapons, 1):
                equipped = " [EQUIPPED]" if weapon == self.equipped_weapon else ""
                print(f"  {i}. {weapon.getDescription()}{equipped}")
        
        # Display armors
        armors = self.getArmors()
        if armors:
            print(f"\nARMORS ({len(armors)}):")
            print("-" * 60)
            for i, armor in enumerate(armors, 1):
                equipped = " [EQUIPPED]" if armor == self.equipped_armor else ""
                print(f"  {i}. {armor.getDescription()}{equipped}")
        
        # Display consumables
        consumables = self.getConsumables()
        if consumables:
            print(f"\nCONSUMABLES ({len(consumables)}):")
            print("-" * 60)
            for i, consumable in enumerate(consumables, 1):
                print(f"  {i}. {consumable.getDescription()}")
        
        if not self.items:
            print("\n  [Inventory empty]")
        
        print("=" * 60 + "\n")
    
    def displayCompact(self):
        weapons_count = len(self.getWeapons())
        armors_count = len(self.getArmors())
        consumables_count = len(self.getConsumables())
        
        equipped_info = ""
        if self.equipped_weapon or self.equipped_armor:
            equipped_parts = []
            if self.equipped_weapon:
                equipped_parts.append(f"Weapon: {self.equipped_weapon.name}")
            if self.equipped_armor:
                equipped_parts.append(f"Armor: {self.equipped_armor.name}")
            equipped_info = f" | Equipped: {', '.join(equipped_parts)}"
        
        print(f"Inventory: {len(self.items)}/{self.MAX_SLOTS} | "
              f"Weapons:{weapons_count} Armors:{armors_count} Consumables:{consumables_count}{equipped_info}")
