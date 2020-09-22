class Player:
    def __init__(self, name="no name", alignment=None, role=None):
        self.alignment = alignment
        self.role = role
        self.name = name
    
    def __str__(self):
        return self.name
    
    def doNightAction(self,game=None):
        if(self.role != None):
            self.role.doNightAction(game=game,player_doing_action=self)
    
    def claimInFormal(self,game=None):
        if(game == None):
            raise Exception("No game when claiming")
        
        if(self.role != None):
            return (game.alignments[0],self.role.claim(game=game))
        else:
            return (game.alignments[0],None)