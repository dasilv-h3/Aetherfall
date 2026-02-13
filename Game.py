from zone.ZoneState import VillageState, ZoneState
from Utils import inputMenu
from entity.Character import Character
from inventory.InventoryMenu import InventoryMenu

class Game:
    def __init__(self, character: Character, enemy_factory, starting_location: "ZoneState"):
        self.character = character
        self.enemy_factory = enemy_factory
        self.location = starting_location
    
    def run(self):
        self.location.onEnter(self)

        while self.character.hp > 0:
            if isinstance(self.location, VillageState):
                self.villageMenu(self.location)
            else:
                self.exploreMenu()
        
        print("Game Over! Your character has been defeated.")
        exit(0)
    
    def villageMenu(self, village: VillageState):
        choice = inputMenu("You are in the village. What would you like to do?", [
            "Talk to villager", 
            "Visit the merchant", 
            "Open inventory",
            "View stats",
            "Explore the world !", 
            "Quit game"
        ])

        if choice == 1:
            print("You talk to the villagers and learn about the dangers lurking in the nearby forest.") # TODO : Add more dialogue options and interactions
            village.strat.talkToVillagers().execute(self)
        elif choice == 2:
            print("You visit the merchant and browse their wares. You can buy potions, weapons, and armor to help you on your journey.") # TODO : Implement shop system
            village.strat.merchantEvent().execute(self)
        elif choice == 3:
            InventoryMenu.open(self.character)
        elif choice == 4:
            self.character.displayStats()
        elif choice == 5:
            print("You leave the village and head towards the forest, ready to face the challenges ahead.") # TODO : Implement zone transition logic
            self.travelMenu()
        elif choice == 6:
            print("Thank you for playing! Goodbye.")
            exit(0)
    
    def travelMenu(self):
        current = self.location

        keys = list(current.connections.keys())
        labels = []
        for key in keys:
            zone = current.connections[key]
            locked = not zone.canEnter(self)
            labels.append(f"{zone.name} {'(Locked)' if locked else ''}")
        
        choice = inputMenu("Where would you like to go?", labels + ["Stay here"])
        if choice == len(labels) + 1:
            print("You decide to stay in the village for now.")
            return
        
        destination_key = keys[choice - 1]
        destination = current.connections[destination_key]
        print(f"You travel to the {destination.name}.")
        self.location = destination
        self.location.onEnter(self)

    def exploreMenu(self):
        print(f"You are in ! {self.location.name}. (HP: {self.character.hp}/{self.character.hpMax})")
        choice = inputMenu("What would you like to do?", [
            "Continue exploring", 
            "Open inventory",
            "View stats",
            "Return to village"
        ])

        if choice == 1:
            print("You continue exploring the area")  
            event = self.location.nextEvent(self)
            if event:
                event.execute(self)
        elif choice == 2:
            InventoryMenu.open(self.character)
        elif choice == 3:
            self.character.display_stats()
        elif choice == 4:
            print("You decide to return to the village to rest and resupply.")
            self.location = self.location.connections["village"]
            self.location.onEnter(self)
           