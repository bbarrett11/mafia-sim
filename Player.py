import random, copy
from Alignment import Alignment
from Role import Role
from Strategy import Strategy
class Player:
    def __init__(self, name: str = "no name", alignment: Alignment = None, role: Role = None, strategy: Strategy = None):
        self.alignment = alignment
        self.role = copy.deepcopy(role)
        self.strategy = copy.deepcopy(strategy)
        self.strategy.role = self.role
        self.role.strategy = self.strategy
        self.name = name
        # Role results if they exist
        self.results = []
        # Initialized on game creation
        self.game = None
        
    def __str__(self) -> str:
        return self.name
    
    def doNightAction(self):
        if(self.role != None):
            self.role.doNightAction()
    
    def claimInFormal(self) -> dict:
        if(self.game == None):
            raise Exception("No game when claiming")
        
        # No PR Claims for now
        if(False):
            return {"alignment": self.game.setup.town_type, "role": self.role.claim()}
        else:
            return {"alignment": self.game.setup.town_type, "role": self.role.claim()}
