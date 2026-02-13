from Utils import inputMenu
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Character import Character

class InventoryMenu:    
    @staticmethod
    def open(character: "Character"):
        while True:
            print("\n")
            character.inventory.display()
            
            choice = inputMenu(
                "What would you like to do?",
                [
                    "Equip a weapon",
                    "Equip armor", 
                    "Use a consumable",
                    "Unequip weapon",
                    "Unequip armor",
                    "Drop an item",
                    "View my stats",
                    "Back"
                ]
            )
            
            if choice == 1:
                InventoryMenu.equipWeaponMenu(character)
            elif choice == 2:
                InventoryMenu.equipArmorMenu(character)
            elif choice == 3:
                InventoryMenu.useConsumableMenu(character)
            elif choice == 4:
                character.inventory.unequipWeapon()
            elif choice == 5:
                character.inventory.unequipArmor()
            elif choice == 6:
                InventoryMenu.dropItemMenu(character)
            elif choice == 7:
                character.displayStats()
            elif choice == 8:
                break
    
    @staticmethod
    def equipWeaponMenu(character: "Character"):
        weapons = character.inventory.getWeapons()
        
        if not weapons:
            print("You have no weapons in your inventory.")
            return
        
        labels = []
        for weapon in weapons:
            equipped = " [EQUIPPED]" if weapon == character.inventory.equippedWeapon else ""
            can_equip = " Insufficient level" if not weapon.canUse(character) else ""
            labels.append(f"{weapon.getDescription()}{equipped}{can_equip}")
        
        choice = inputMenu("Which weapon would you like to equip?", labels + ["Cancel"])
        
        if choice <= len(weapons):
            weapon = weapons[choice - 1]
            character.inventory.equipWeapon(weapon, character)
    
    @staticmethod
    def equipArmorMenu(character: "Character"):
        armors = character.inventory.getArmors()
        
        if not armors:
            print("You have no armors in your inventory.")
            return
        
        labels = []
        for armor in armors:
            equipped = " [EQUIPPED]" if armor == character.inventory.equippedArmor else ""
            can_equip = " Insufficient level" if not armor.canUse(character) else ""
            labels.append(f"{armor.getDescription()}{equipped}{can_equip}")
        
        choice = inputMenu("Which armor would you like to equip?", labels + ["Cancel"])
        
        if choice <= len(armors):
            armor = armors[choice - 1]
            character.inventory.equipArmor(armor, character)
    
    @staticmethod
    def useConsumableMenu(character: "Character"):
        consumables = character.inventory.getConsumables()
        
        if not consumables:
            print("You have no consumables in your inventory.")
            return
        
        labels = []
        for consumable in consumables:
            canUse = " Insufficient level" if not consumable.canUse(character) else ""
            labels.append(f"{consumable.getDescription()}{canUse}")
        
        choice = inputMenu("Which consumable would you like to use?", labels + ["Cancel"])
        
        if choice <= len(consumables):
            consumable = consumables[choice - 1]
            character.inventory.useConsumable(consumable, character)
    
    @staticmethod
    def dropItemMenu(character: "Character"):
        if not character.inventory.items:
            print("Your inventory is empty.")
            return
        
        labels = []
        for item in character.inventory.items:
            item_type = "⚔️" if hasattr(item, 'getDescription') and 'Weapon' in item.getDescription() else \
                "🛡️" if hasattr(item, 'getDescription') and 'Armor' in item.getDescription() else "🧪"
            labels.append(f"{item_type} {item.name}")
        
        choice = inputMenu("Which item would you like to drop?", labels + ["Cancel"])
        
        if choice <= len(character.inventory.items):
            item = character.inventory.items[choice - 1]
            
            # Ask for confirmation
            confirm = inputMenu(
                f"Are you sure you want to drop {item.name}?",
                ["Yes", "No"]
            )
            
            if confirm == 1:
                # Unequip the item if it is equipped
                if item == character.inventory.equippedWeapon:
                    character.inventory.unequipWeapon()
                elif item == character.inventory.equippedArmor:
                    character.inventory.unequipArmor()
                
                character.inventory.remove_item(item)
    
    @staticmethod
    def combatConsumableMenu(character: "Character"):
        consumables = character.inventory.getConsumables()
        
        if not consumables:
            print("You have no consumables in your inventory.")
            return None
        
        labels = []
        for consumable in consumables:
            labels.append(f"{consumable.getDescription()}")
        
        choice = inputMenu("Which consumable would you like to use?", labels + ["Cancel"])
        
        if choice <= len(consumables):
            consumable = consumables[choice - 1]
            result = character.inventory.useConsumable(consumable, character)
            return result
        
        return None
