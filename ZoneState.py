import Game

class ZoneState():
    def __init__(self, name: str):
        self.name = name
        self.connections = {}

    def connect(self, key: str, zone: "ZoneState") -> None:
        self.connections[key] = zone
    
    def onEnter(self, game: "Game") -> None:
        print(f"\nYou enter the {self.name}.")

    def canEnter(self, game: "Game") -> bool:
        return True

class VillageState(ZoneState):
    def __init__(self):
        super().__init__(name="Village")

class ForestState(ZoneState):
    def __init__(self):
        super().__init__(name="Forest")

    def onEnter(self, game: "Game") -> None:
        super().onEnter(game)
        print("You enter in the forest")