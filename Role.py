import re
class Role:
    def __init__(self,name="",active_n0=True):
        self.name=name
        self.active_n0=active_n0
        self.modified = False
        
    def doNightAction(self,game=None, player_doing_action=None):
        # TO BE IMPLEMENTED IN CHILD CLASSES
        if(game == None or player_doing_action == None):
            raise Exception("Game does not exist while doing action")
    
    def claim(self,game=None):
        if(game == None ):
            raise Exception("Game does not exist while claiming")
    def __str__(self):
        return self.name
        
        