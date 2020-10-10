from MafiaGame import MafiaGame

class MafiaSetup:
    def __init__(self, players=[], teams=[]):
        self.teams = teams
        self.players = players
    
    def simulate(self) -> MafiaGame:
        game = MafiaGame(self)
        game.play()
        return game
    
    def countAlignment(self, alignment=None) -> int:
        if(not alignment):
            raise Exception("Counting alignment of None")
        num_same=0
        for player in self.players:
            if player.alignment.name == alignment.name:
                num_same+=1
        return num_same
    
    def describe(self):
        for player in self.players:
            print(f"{player.alignment} {player.role}")