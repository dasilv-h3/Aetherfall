class Character:
    def __init__(
            self, 
            name:str,
            type:str,
            defense:int = 10,
            level:int = 0,
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
        return super().__init__(name=name, type="Warrior", defense= 0, hp= 100 + (100*0.5), hpMax= 100 + (100*0.5), strength=50)
    
    def attack(self, enemy):
        print(f"{self.name} lvl {self.level} attacks {enemy.name}!")
        damage = max(0, self.strength - enemy.defense)
        enemy.hp -= damage
        print(f"{enemy.name} takes {damage} damage! (HP: {enemy.hp}/{enemy.hpMax})")
        return enemy
    

    def skill1(self):
        pass
    
    def skill2(self):
        pass


class Mage(Character):

    def __init__(self, name):
        return super().__init__(name=name, type="Warrior", defense= 50, hp= 100 * (100*0.5), hpMax= 100 * (100*0.5), strength=50)
    
    def attack(self, enemy):
        print(f"{self.name} lvl {self.level} attacks {enemy.name}!")
        damage = max(0, self.strength - enemy.defense)
        enemy.hp -= damage
        print(f"{enemy.name} takes {damage} damage! (HP: {enemy.hp}/{enemy.hpMax})")
        return enemy
    

    def skill1(self):
        pass
    
    def skill2(self):
        pass


class Thief(Character):

    def __init__(self, name):
        return super().__init__(name=name, type="T", defense= 50, hp= 100 * (100*0.5), hpMax= 100 * (100*0.5), strength=50)
    
    def attack(self, enemy):
        print(f"{self.name} lvl {self.level} attacks {enemy.name}!")
        damage = max(0, self.strength - enemy.defense)
        enemy.hp -= damage
        print(f"{enemy.name} takes {damage} damage! (HP: {enemy.hp}/{enemy.hpMax})")
        return enemy
    

    def skill1(self):
        pass
    
    def skill2(self):
        pass