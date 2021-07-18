from Role import Role
from Action import ActionType, Action
class Vigi(Role):
    # Normal medic: cannot save themself
    def __init__(self, name='', active_n0=True,charges=1):
        super().__init__(name=name, active_n0=active_n0)
        self.charges = charges
        
    def doNightAction(self):
        super().doNightAction()
        if(not self.owner in self.game.alive_players):
            return
        
        if(self.charges > 0 and self.strategy.doIActivate(self.game)):
            target = self.strategy.whoDoITarget(self.game)
            self.game.addNightAction(Action(action_type=ActionType.KP,target=target,owner=self.owner))
            self.charges-=1
    
    def claim(self):
        super().claim()
        return {"role": self,"results": self.owner.results}       
        