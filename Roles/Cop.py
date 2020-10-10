from Role import Role
from Action import ActionType, Action
class Cop(Role):
    # Alignment Cop: gets simple alignment check
    def __init__(self, name='', active_n0=True,charges=999, target_self=False):
        super().__init__(name=name, active_n0=active_n0)
        self.charges = charges
        self.target_self = target_self
        # Results given in form (Player, Alignment)
        
    def doNightAction(self):
        super().doNightAction()
        if(self.charges > 0):
            if(not self.target_self):
                targetable_players = [x for x in self.game.alive_players if x != self.owner]
            else:
                targetable_players = [x for x in self.game.alive_players]
            target = self.game.chooseRandPlayer(targetable_players)
            self.game.addNightAction(Action(action_type=ActionType.CHECK, target=target, owner=self.owner))
            self.charges-=1

    def claim(self):
        super().claim()
        return {"role": self,"results": self.owner.results}