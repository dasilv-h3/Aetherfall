from StatModifier import StatCalculator
from inventory.Inventory import Inventory

class Character:
    def __init__(
            self, 
            name:str,
            type:str,
            defense:int = 10,
            level:int = 1,
            xp:int = 0,
            hp:int = 100,
            hpMax:int = 100,
            strength:int = 20,
            intelligence:int = 20,
            agility:int = 30,
            critChance:int = 0
        ):
        self.name = name
        self.level = level
        self.xp = xp
        self.type = type
        self.hp = hp
        self.hpMax = hpMax
        self.strength = strength
        self.defense = defense
        self.intelligence = intelligence
        self.agility = agility
        self.critChance = critChance

        self.inventory = Inventory()
    
    def getEffectiveStat(self, stat_name: str) -> int:
        return StatCalculator.calculateStat(self, stat_name)
    
    def displayStats(self):
        StatCalculator.displayStats(self)

    def attack(self):
        pass
    
    def defense(self):
        pass

    def skill1(self):
        pass

    def skill2(self):
        pass



class Warrior(Character):

    def __init__(self, name):
        return super().__init__(name=name, type="Warrior", defense=12, hp=120, hpMax=120, strength=25, critChance=5)
    
    def attack(self, enemy):
        print(f"{self.name} lvl {self.level} attacks {enemy.name}!")
        # Utilise les stats effectives (base + équipement)
        effective_strength = self.getEffectiveStat('strength')
        effective_defense = enemy.getEffectiveStat('defense') if hasattr(enemy, 'getEffectiveStat') else enemy.defense
        damage = max(0, effective_strength - effective_defense)
        enemy.hp -= damage
        print(f"{enemy.name} takes {damage} damage! (HP: {enemy.hp}/{enemy.hpMax})")
        return enemy
    

    def skill1(self):
        pass
    
    def skill2(self):
        pass


class Mage(Character):

    def __init__(self, name):
        return super().__init__(name=name, type="Mage", defense=5, hp=80, hpMax=80, intelligence=30, strength=10)
    
    def attack(self, enemy):
        print(f"{self.name} lvl {self.level} casts a spell on {enemy.name}!")
        # Utilise l'intelligence pour les mages
        effective_intelligence = self.getEffectiveStat('intelligence')
        effective_defense = enemy.getEffectiveStat('defense') if hasattr(enemy, 'getEffectiveStat') else enemy.defense
        damage = max(0, effective_intelligence - effective_defense)
        enemy.hp -= damage
        print(f"{enemy.name} takes {damage} magical damage! (HP: {enemy.hp}/{enemy.hpMax})")
        return enemy
    

    def skill1(self):
        pass
    
    def skill2(self):
        pass


class Thief(Character):

    def __init__(self, name):
        return super().__init__(name=name, type="Thief", defense=8, hp=100, hpMax=100, agility=25, strength=18, critChance=15)
    
    def attack(self, enemy):
        print(f"{self.name} lvl {self.level} strikes {enemy.name} swiftly!")
        # Utilise l'agilité + force pour les voleurs
        effective_agility = self.getEffectiveStat('agility')
        effective_strength = self.getEffectiveStat('strength')
        effective_defense = enemy.getEffectiveStat('defense') if hasattr(enemy, 'getEffectiveStat') else enemy.defense
        damage = max(0, (effective_strength + effective_agility // 2) - effective_defense)
        enemy.hp -= damage
        print(f"{enemy.name} takes {damage} damage! (HP: {enemy.hp}/{enemy.hpMax})")
        return enemy
    

    def skill1(self):
        pass
    
    def skill2(self):
        pass