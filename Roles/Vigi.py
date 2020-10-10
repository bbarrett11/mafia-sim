from Role import Role
from Action import ActionType, Action
class Vigi(Role):
    # Normal medic: cannot save themself
    def __init__(self, name='', active_n0=True,charges=1):
        super().__init__(name=name, active_n0=active_n0)
        self.charges = charges
        
    def doNightAction(self):
        super().doNightAction()
        if(self.charges > 0 ):
            targetable_players = [x for x in self.game.alive_players if x != self.owner]
            target = self.game.chooseRandPlayer(targetable_players)
            self.game.addNightAction(Action(action_type=ActionType.KP,target=target))
            self.charges-=1
    
    def claim(self):
        super().claim()
        return {"role": self,"results": self.owner.results}       
        