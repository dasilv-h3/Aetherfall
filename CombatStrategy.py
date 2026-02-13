import random
from typing import TYPE_CHECKING
from Utils import inputMenu

if TYPE_CHECKING:
    from entity.Character import Character
    from entity.EnemyFactory import Enemy

class CombatAction:
    def __init__(self, name: str):
        self.name = name
    
    def execute(self, attacker, defender, combat_state) -> dict:
        pass

class AttackAction(CombatAction):
    def __init__(self):
        super().__init__("Attack")
    
    def execute(self, attacker, defender, combat_state) -> dict:
        if hasattr(attacker, 'getEffectiveStat'):
            attack_stat = attacker.getEffectiveStat('strength')
        else:
            attack_stat = getattr(attacker, 'strength', 0)
        
        if hasattr(defender, 'getEffectiveStat'):
            defense_stat = defender.getEffectiveStat('defense')
        else:
            defense_stat = getattr(defender, 'defense', 0)
        
        # Applique la réduction de défense si le défenseur se défend
        if combat_state.get('defender_is_defending', False):
            defense_stat = int(defense_stat * 1.5)
        
        # Calcul des dégâts avec variance aléatoire (±10%)
        base_damage = max(0, attack_stat - defense_stat)
        variance = random.uniform(0.9, 1.1)
        damage = int(base_damage * variance)
        
        crit_chance = getattr(attacker, 'critChance', 0)
        is_crit = random.random() < (crit_chance / 100)
        
        if is_crit:
            damage = int(damage * 1.5)
            result_text = f"CRITICAL HIT ! {attacker.name} deals {damage} damage to {defender.name}!"
        else:
            result_text = f"{attacker.name} deals {damage} damage to {defender.name}!"
        
        defender.hp -= damage
        
        return {
            'damage': damage,
            'is_crit': is_crit,
            'text': result_text,
            'defender_hp': max(0, defender.hp)
        }

class DefendAction(CombatAction):
    def __init__(self):
        super().__init__("Defend")
    
    def execute(self, attacker, defender, combat_state) -> dict:
        combat_state['attacker_is_defending'] = True
        result_text = f"{attacker.name} takes a defensive stance! Defense increased for the next turn."
        
        return {
            'damage': 0,
            'text': result_text,
            'is_defending': True
        }

class SkillAction(CombatAction):
    def __init__(self, skill_name: str, skill_function, description: str = ""):
        super().__init__(skill_name)
        self.skill_function = skill_function
        self.description = description
    
    def execute(self, attacker, defender, combat_state) -> dict:
        return self.skill_function(attacker, defender, combat_state)

class UseItemAction(CombatAction):
    def __init__(self, item):
        super().__init__(f"Use {item.name}")
        self.item = item
    
    def execute(self, attacker, defender, combat_state) -> dict:
        from item.Item import Consumable
        
        if isinstance(self.item, Consumable):
            if "damage" in self.item.affected_stats:
                damage = self.item.value
                defender.hp -= damage
                result_text = f"{attacker.name} uses {self.item.name}! {defender.name} takes {damage} damage!"
                self.item.is_used = True
                return {
                    'damage': damage,
                    'text': result_text,
                    'defender_hp': max(0, defender.hp),
                    'item_used': True
                }
            elif "hp" in self.item.affected_stats:
                old_hp = attacker.hp
                attacker.hp = min(attacker.hp + self.item.value, attacker.hpMax)
                healed = attacker.hp - old_hp
                result_text = f"{attacker.name} uses {self.item.name} and recovers {healed} HP! (HP: {attacker.hp}/{attacker.hpMax})"
                self.item.is_used = True
                return {
                    'damage': 0,
                    'healed': healed,
                    'text': result_text,
                    'attacker_hp': attacker.hp,
                    'item_used': True
                }
            else:
                result_text = f"{attacker.name} uses {self.item.name}!"
                self.item.is_used = True
                return {
                    'damage': 0,
                    'text': result_text,
                    'item_used': True
                }

class CombatSystem:    
    def __init__(self, player: "Character", enemy: "Enemy"):
        self.player = player
        self.enemy = enemy
        self.turn_count = 0
        self.combat_state = {
            'player_is_defending': False,
            'enemy_is_defending': False
        }
        self.combat_log = []
    
    def start_combat(self) -> bool:
        print("\n" + "="*60)
        print(f"FIGHT VS {self.enemy.name.upper()} (Level {self.enemy.level})")
        print("="*60)
        
        while self.player.hp > 0 and self.enemy.hp > 0:
            self.turn_count += 1
            self.display_combat_status()
            
            if not self.player_turn():
                return False
            
            if self.enemy.hp <= 0:
                self.victory()
                return True
            
            self.enemy_turn()
            
            if self.player.hp <= 0:
                self.defeat()
                return False
        
        return False
    
    def display_combat_status(self):
        print(f"\n--- Turn {self.turn_count} ---")
        print(f"{self.player.name}: {self.player.hp}/{self.player.hpMax} HP")
        print(f"{self.enemy.name}: {self.enemy.hp}/{self.enemy.hpMax} HP")
        
        if self.combat_state.get('player_is_defending'):
            print(f"{self.player.name} is in a defensive stance")
        if self.combat_state.get('enemy_is_defending'):
            print(f"{self.enemy.name} is in a defensive stance")
        print()
    
    def player_turn(self) -> bool:
        # Reset the defending state from the previous turn
        defending_last_turn = self.combat_state.get('player_is_defending', False)
        self.combat_state['player_is_defending'] = False
        
        if defending_last_turn:
            print(f"{self.player.name} returns to an offensive stance.\n")
        
        actions = [
            "Attack",
            "Skill",
            "Use an item",
            "Defend"
        ]
        
        choice = inputMenu(f"What do you want to do?", actions)
        
        if choice == 1:
            action = AttackAction()
            result = action.execute(self.player, self.enemy, self.combat_state)
            print(f"\n{result['text']}")
            print(f"{self.enemy.name}: {result['defender_hp']}/{self.enemy.hpMax} HP")
        
        elif choice == 2:
            return self.use_skill()
        
        elif choice == 3:
            return self.use_item()
        
        elif choice == 4:
            action = DefendAction()
            result = action.execute(self.player, self.enemy, self.combat_state)
            print(f"\n{result['text']}")
        
        return True
    
    def use_skill(self) -> bool:
        print("No skills not implemented!")
        return self.player_turn()
        
    def use_item(self) -> bool:      
        consumables = self.player.inventory.getConsumables()
        
        if not consumables:
            print("No consumables available!")
            return self.player_turn()
        
        labels = [consumable.getDescription() for consumable in consumables]
        labels.append("Back")
        
        choice = inputMenu("Which item do you want to use?", labels)
        
        if choice > len(consumables):
            return self.player_turn()
        
        item = consumables[choice - 1]
        action = UseItemAction(item)
        result = action.execute(self.player, self.enemy, self.combat_state)
        
        print(f"\n{result['text']}")

        if result.get('item_used'):
            self.player.inventory.removeItem(item)
        
        return True
    
    def enemy_turn(self):
        # Réinitialise l'état de défense du tour précédent
        defending_last_turn = self.combat_state.get('defender_is_defending', False)
        self.combat_state['defender_is_defending'] = False
        
        if defending_last_turn:
            print(f"\n{self.enemy.name} returns to an offensive stance.\n")
        
        print(f"\n--- {self.enemy.name}'s Turn ---")
        
        # The enemy chooses an action
        action_choice = random.random()
        
        if action_choice < 0.7:  # 70% chance to attack
            action = AttackAction()
            result = action.execute(self.enemy, self.player, self.combat_state)
            print(f"{result['text']}")
            print(f"{self.player.name}: {result['defender_hp']}/{self.player.hpMax} HP")
        
        elif action_choice < 0.85 or not hasattr(self.enemy, 'skill1'):  # 15% chance de se défendre
            action = DefendAction()
            result = action.execute(self.enemy, self.player, self.combat_state)
            result['text'] = result['text'].replace('attacker_is_defending', 'defender_is_defending')
            self.combat_state['defender_is_defending'] = True
            self.combat_state['attacker_is_defending'] = False
            print(f"{result['text']}")
        
        else:  # 15% chance d'utiliser une compétence
            if hasattr(self.enemy, 'skill1'):
                print(f"{self.enemy.name} uses a special skill!")
                self.enemy.skill1(self.player)
            else:
                print(f"{self.enemy.name} tries to use a skill but fails!")
    
    def victory(self):
        print("\n" + "="*60)
        print("🎉 VICTORY! 🎉")
        print(f"You have defeated {self.enemy.name}!")
        
        # Calcul de l'XP et du loot
        xp_gained = self.enemy.level * random.randint(5, 12) + 20
        self.player.xp += xp_gained
        print(f"ou gain {xp_gained} experience points!")
        
        print("="*60 + "\n")

    def defeat(self):
        print("\n" + "="*60)
        print("💀 DEFEAT... 💀")
        print(f"{self.player.name} was defeated by {self.enemy.name}...")
        print("="*60 + "\n")
