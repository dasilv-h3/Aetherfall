import random

class Enemy:
    def __init__(
        self,
        name: str,
        level: int,
        type: str,
        hp: int,
        hpMax: int,
        strength: int,
        defense: int,
        minNumberOfAttacks: int = 1,
        maxNumberOfAttacks: int = 1,
        attackTypeResistance: list = None,
    ):
        self.name = name
        self.level = level
        self.type = type
        self.hp = hp
        self.hpMax = hpMax
        self.strength = strength
        self.defense = defense
        self.minNumberOfAttacks = minNumberOfAttacks
        self.maxNumberOfAttacks = maxNumberOfAttacks
        self.attackTypeResistance = attackTypeResistance if attackTypeResistance is not None else []

    def attack(self, character):
        print(f"{self.name} lvl {self.level} attacks {character.name}!")
        damage = max(0, self.strength - character.defense)
        character.hp -= damage
        print(f"{character.name} takes {damage} damage! (HP: {character.hp}/{character.hpMax})")
        return character
    
    def defend(self, character):
        print(f"{self.name} lvl {self.level} defend from {character.name} attack!")
    
    def skill1(self, character):
        return character
        
    def skill2(self, character):
        return character

class Wolf(Enemy):
    def __init__(self, level: int):
        super().__init__(name="Wolf", level=level, type="Beast", hp=40 + (level * 8), hpMax=40 + (level * 8), strength=12 + (level * 2), defense=3 + level, minNumberOfAttacks=1, maxNumberOfAttacks=1 + (level // 3))
    
    def attack(self, character):
        number_of_attacks = self._roll_number_of_attacks()
        print(f"{self.name} lvl {self.level} attacks {character.name} {number_of_attacks} time(s)!")

        for _ in range(number_of_attacks):
            super().attack(character)
        return character
    
    def _roll_number_of_attacks(self):
        return random.randint(self.minNumberOfAttacks, self.maxNumberOfAttacks)

class Bandit(Enemy):
    def __init__(self, level: int):
        super().__init__(name="Bandit", level=level, type="Human", hp=50 + (level * 10), hpMax=50 + (level * 10), strength=14 + (level * 3), defense=6 + (level * 2))
    
    def attack(self, character):
        chance_to_steal = random.random() < 0.01 * self.level # 1% chance to steal per level
        
        if chance_to_steal:
            print(f"{self.name} steals from {character.name}!") # TODO : Implement stealing logic here (e.g., reduce character's gold or items)
        else:
            super().attack(character)
        
        return character

class Skeleton(Enemy):
    def __init__(self, level: int):
        super().__init__(name="Skeleton", level=level, type="Skeleton", hp=45 + (level * 10), hpMax=45 + (level * 10), strength=10 + (level * 2), defense=8 + (level * 2), attackTypeResistance=["Physical"])

class CorruptedChampion(Enemy):
    def __init__(self, level: int):
        super().__init__(name="Corrupted Champion", level=level, type="Demon", hp=80 + (level * 15), hpMax=80 + (level * 15), strength=18 + (level * 4), defense=10 + (level * 2))
    
    def skill1(self, character):
        damage = max(0, (self.strength * 1.5) - character.defense)
        character.hp -= damage
        print(f"{character.name} takes {damage} damage from Corrupted Strike! (HP: {character.hp}/{character.hpMax})")
        return character

class Boss(Enemy):
    def __init__(self, level: int):
        self.boss_phase = 1
        super().__init__(name="Boss", level=level, type="Boss", hp=150 + (level * 30), hpMax=150 + (level * 30), strength=25 + (level * 5), defense=15 + (level * 3))

    def skill1(self, character):
        damage = max(0, (self.strength * 2) - character.defense)
        character.hp -= damage
        print(f"{character.name} takes {damage} damage from Boss's powerful strike! (HP: {character.hp}/{character.hpMax})")
        return character

    def skill2(self, character):
        if (self.boss_phase == 1):
            print(f"{self.name} tries to use a sweeping attack, but it's not effective in phase 1!")
        damage = max(0, (self.strength * 1.5) - character.defense)
        character.hp -= damage
        print(f"{character.name} takes {damage} damage from Boss's sweeping attack! (HP: {character.hp}/{character.hpMax})")
        return character

    def check_phase_transition(self):
        if self.hp <= self.hpMax * 0.5 and self.boss_phase == 1:
            self.boss_phase = 2
            self.strength += 10
            self.defense += 5
            print(f"{self.name} enrages and enters phase 2! Strength and defense increased!")

class EnemyFactory:
    def create_enemy(self, enemy_type: str, level: int) -> Enemy:
        if enemy_type == "Wolf":
            return Wolf(level)
        elif enemy_type == "Bandit":
            return Bandit(level)
        elif enemy_type == "Skeleton":
            return Skeleton(level)
        elif enemy_type == "Corrupted Champion":
            return CorruptedChampion(level)
        elif enemy_type == "Boss":
            return Boss(level)
        else:
            raise ValueError(f"Unknown enemy type: {enemy_type}")