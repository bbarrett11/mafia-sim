from Role import Role
from Action import ActionType, Action
class Vigi(Role):
    # Normal medic: cannot save themself
    def __init__(self, name='', active_n0=True,charges=1):
        super().__init__(name=name, active_n0=active_n0)
        self.charges = charges
        
    def doNightAction(self,game=None,owner=None):
        super().doNightAction(game=game, owner=owner)
        if(self.charges > 0 ):
            targetable_players = [x for x in game.alive_players if x != owner]
            target = game.chooseRandPlayer(targetable_players)
            game.addNightAction(Action(action_type=ActionType.KP,target=target))
            self.charges-=1
    
    def claim(self,game=None):
        super().claim(game=game)
        
        return self
        
        