from Role import Role
from Action import ActionType, Action
class Possum(Role):
    # Normal medic: cannot save themself
    def __init__(self, name='', active_n0=True):
        super().__init__(name=name, active_n0=active_n0)
        self.prev_target = None
        
    def doNightAction(self):
        super().doNightAction()
        if(self.prev_target in self.game.hidden_players):
            self.game.alive_players.append(self.prev_target)
            self.game.hidden_players.remove(self.prev_target)
        
        if(not self.owner in self.game.alive_players):
            return
        elif(not (self.game.checkDayNight(0) or self.game.checkDayNight(1))):
            return
        
        targetable_players = [x for x in self.game.alive_players if x != self.owner and x != self.prev_target]
        target = self.game.chooseRandPlayer(targetable_players)
        self.prev_target = target
        self.game.alive_players.remove(target)
        self.game.hidden_players.append(target)
        self.game.addNightAction(Action(action_type=ActionType.INFO,owner=self.owner,log=f"Possum had {target} play dead"))

    def claim(self):
        super().claim()
        return {"role": self,"results": self.owner.results}   