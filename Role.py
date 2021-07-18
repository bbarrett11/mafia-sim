import re
class Role:
    def __init__(self,name:str="",active_n0:bool=True):
        self.name      = name
        self.active_n0 = active_n0
        self.modified  = False
        # Not initialized b/c game/player hasn't been created yet
        # is initialized in Player
        self.owner = None
        self.game  = None
        self.has_exile_action = False
        # set by player
        self.strategy = None
        
    def doNightAction(self):
        # TO BE IMPLEMENTED IN CHILD CLASSES
        if(self.game == None or self.owner == None):
            raise Exception("Game or player does not exist while doing action")
    
    def claim(self):
        if(self.game == None or self.owner == None ):
            raise Exception("Game or player does not exist while claiming")

    def __str__(self) -> str:
        return self.name
    
    def __eq__(self,other) -> bool:
        if(not other or not other.name):
            return False
        return self.name == other.name