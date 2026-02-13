import os
import json
from enum import Enum
from datetime import datetime
from entity.Character import Character, Warrior, Mage, Thief
from inventory.Inventory import Inventory
from item.Item import Weapon, Armor, Consumable, ModifierType
from Utils import inputMenu


SAVES_DIR = os.path.join(os.path.dirname(__file__), 'saves')


def serialize(obj):
    if isinstance(obj, Enum):
        return obj.value
    if hasattr(obj, '__dict__'):
        return obj.__dict__
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def _deserialize_item(data: dict):
    item_type = data["item_type"]
    modifier_type = ModifierType(data["modifier_type"])

    if item_type == "weapon":
        return Weapon(
            name=data["name"],
            minimal_level=data["minimal_level"],
            modifier_type=modifier_type,
            value=data["value"],
            affected_stats=data["affected_stats"],
            apparition_rate=data["apparition_rate"]
        )
    elif item_type == "armor":
        return Armor(
            name=data["name"],
            minimal_level=data["minimal_level"],
            modifier_type=modifier_type,
            value=data["value"],
            affected_stats=data["affected_stats"],
            apparition_rate=data["apparition_rate"]
        )
    elif item_type == "consumable":
        c = Consumable(
            name=data["name"],
            minimal_level=data["minimal_level"],
            modifier_type=modifier_type,
            value=data["value"],
            affected_stats=data["affected_stats"],
            apparition_rate=data["apparition_rate"]
        )
        c.is_used = data.get("is_used", False)
        return c
    return None


def _deserialize_character(data: dict) -> Character:
    """Convertit un dict JSON en objet Character (Warrior/Mage/Thief)."""
    char_type = data["type"]
    name = data["name"]

    class_map = {"Warrior": Warrior, "Mage": Mage, "Thief": Thief}
    cls = class_map.get(char_type)

    if cls:
        character = cls(name)
    else:
        character = Character(name=name, type=char_type)

    # Restaure les stats sauvegardees
    character.level = data["level"]
    character.xp = data["xp"]
    character.hp = data["hp"]
    character.hpMax = data["hpMax"]
    character.strength = data["strength"]
    character.defense = data["defense"]
    character.intelligence = data["intelligence"]
    character.agility = data["agility"]
    character.critChance = data["critChance"]

    # Restaure l'inventaire
    inv_data = data.get("inventory", {})
    character.inventory = Inventory()

    for item_data in inv_data.get("items", []):
        item = _deserialize_item(item_data)
        if item:
            character.inventory.items.append(item)

    if inv_data.get("equipped_weapon"):
        character.inventory.equipped_weapon = _deserialize_item(inv_data["equipped_weapon"])

    if inv_data.get("equipped_armor"):
        character.inventory.equipped_armor = _deserialize_item(inv_data["equipped_armor"])

    return character


class SaveGame:

    def save(self, character: Character):
        os.makedirs(SAVES_DIR, exist_ok=True)
        date = datetime.today().strftime('%d-%m-%Y_%H:%M:%S')
        filepath = os.path.join(SAVES_DIR, f'{character.name}_{character.type}_save-{date}.json')
        with open(file=filepath, mode="w") as f:
            json.dump(character, f, indent=4, default=serialize)
        print(f"Game saved: {os.path.basename(filepath)}")

    def load(self) -> Character | None:
        """Affiche les 5 dernieres sauvegardes et charge celle choisie."""
        if not os.path.isdir(SAVES_DIR):
            print("No saves directory found.")
            return None
        
        save_files = [f for f in os.listdir(SAVES_DIR) if f.endswith('.json')]
        save_files.sort(key=lambda f: os.path.getmtime(os.path.join(SAVES_DIR, f)), reverse=True)

        if not save_files:
            print("No save files found.")
            return None

        last_saves = save_files[:5]
        labels = []
        for f in last_saves:
            display_name = f.replace('.json', '').replace('_save-', ' | ')
            labels.append(display_name)

        choice = inputMenu("Choose a save to load", labels + ["Back"])

        if choice == len(labels) + 1:
            return None

        selected_file = last_saves[choice - 1]
        filepath = os.path.join(SAVES_DIR, selected_file)

        with open(filepath, 'r') as f:
            data = json.load(f)

        character = _deserialize_character(data)
        print(f"\nSave loaded: {character.name} ({character.type}) - Level {character.level}")
        character.displayStats()
        return character