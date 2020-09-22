from Role import Role
from Action import ActionType, Action
class Cop(Role):
    # Alignment Cop: gets simple alignment check
    def __init__(self, name='', active_n0=True,charges=999, target_self=False):
        super().__init__(name=name, active_n0=active_n0)
        self.charges = charges
        self.target_self = target_self
        # Results given in form (Name, Alignment)
        
    def doNightAction(self,game=None,owner=None):
        super().doNightAction(game=game,owner=owner)
        if(self.charges > 0):
            if(not self.target_self):
                targetable_players = [x for x in game.alive_players if x != owner]
            else:
                targetable_players = [x for x in game.alive_players]
            target = game.chooseRandPlayer(targetable_players)
            game.addNightAction(Action(action_type=ActionType.CHECK, target=target, owner=owner))
            self.charges-=1

    def claim(self,game=None):
        super().claim(game=game)
        return self