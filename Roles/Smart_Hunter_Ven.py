from Role import Role
from Action import ActionType, Action
class Smart_Hunter_Ven(Role):
    # Smart Hunter: Has smart shot when dies, if other smart
    # hunter is alive their shot is cancelled
    def __init__(self, name='Smart Hunter', active_n0=False):
        super().__init__(name=name, active_n0=active_n0)
        self.has_exile_action = True
        
    def doNightAction(self):
        super().doNightAction()
        pass
    def doExileAction(self):
        for x in self.game.alive_players:
            if(x.role == self):
                x.role.has_exile_action = False
        
        targetable_players = [x for x in self.game.alive_players if x != self.owner]
        target = self.game.chooseRandPlayer(targetable_players)
        if(target.alignment == self.owner.alignment):
            self.game.confirmTown(target)
        else:
            self.game.exile(target)

    def claim(self):
        super().claim()
        return {"role": self,"results": self.owner.results}
