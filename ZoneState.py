import Game
from ZoneStrategy import ForestStrategy, VillageStrategy, ZoneStrategy

class ZoneState():
    def __init__(self, name: str, strategy: ZoneStrategy):
        self.name = name
        self.strategy = strategy
        self.connections = {}

    def connect(self, key: str, zone: "ZoneState") -> None:
        self.connections[key] = zone
    
    def onEnter(self, game: "Game") -> None:
        print(f"\nYou enter the {self.name}.")
        next_event = self.nextEvent(game)
        if next_event:
            next_event.execute(game)

    def canEnter(self, game: "Game") -> bool:
        return True
    
    def nextEvent(self, game: "Game") -> None:
        return self.strategy.nextEvent(game)

class VillageState(ZoneState):
    def __init__(self):
        super().__init__(name="Village", strategy=VillageStrategy())

    @property
    def strat(self) -> VillageStrategy:
        return self.strategy

class ForestState(ZoneState):
    def __init__(self, enemy_factory):
        super().__init__(name="Forest", strategy=ForestStrategy(enemy_factory))

    def onEnter(self, game: "Game") -> None:
        super().onEnter(game)
        self.strategy.resetRun()
        print("You enter in the forest")