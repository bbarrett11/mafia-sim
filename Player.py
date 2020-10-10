import random, copy
from Alignment import Alignment
from Role import Role
class Player:
    def __init__(self, name: str = "no name", alignment: Alignment = None, role: Role = None):
        self.alignment = alignment
        self.role = copy.deepcopy(role)
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
            return {"alignment": self.game.alignments[0], "role": self.role.claim()}
        else:
            return {"alignment": self.game.alignments[0], "role": self.role.claim()}
