
class MafiaSetup:
    def __init__(self, players=[], day_start = False, town_type = None, mafia_type = None):
        self.players = players
        self.day_start = day_start
        if(not town_type or not mafia_type):
            raise Exception("Town or mafia Faction not recognized")
        self.mafia_type = mafia_type
        self.town_type  = town_type
        self.teams = [self.town_type, self.mafia_type]
        
    def countAlignment(self, alignment=None) -> int:
        if(not alignment):
            raise Exception("Counting alignment of None")
        num_same=0
        for player in self.players:
            if player.alignment == alignment:
                num_same+=1
        return num_same
    
    def describe(self):
        for player in self.players:
            print(f"{str(player.alignment)} {str(player.role)}")