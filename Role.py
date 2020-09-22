import re
class Role:
    def __init__(self,name="",active_n0=True):
        self.name=name
        self.active_n0=active_n0
        self.modified = False
        
    def doNightAction(self,game=None, owner=None):
        # TO BE IMPLEMENTED IN CHILD CLASSES
        if(game == None or owner == None):
            raise Exception("Game or player does not exist while doing action")
    
    def claim(self, game=None, owner=None):
        if(game == None or owner == None ):
            raise Exception("Game or player does not exist while claiming")
    def __str__(self):
        return self.name
        
        