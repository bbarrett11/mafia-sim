from MafiaGame import MafiaGame

class MafiaSetup:
    def __init__(self, players=[], teams=[]):
        self.teams = teams
        self.players = players
    
    def simulate(self):
        game = MafiaGame(self)
        game.play()
        return game
    
    def countAlignment(self, alignment=None):
        if(alignment == None):
            raise Exception("Counting alignment of None")
        num_same=0
        for player in self.players:
            if player.alignment.name == alignment.name:
                num_same+=1
        return num_same