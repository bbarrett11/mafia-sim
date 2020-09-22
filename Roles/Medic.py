from Role import Role
from Action import ActionType, Action
class Medic(Role):
    # Normal medic: cannot save themself
    def __init__(self, name='', active_n0=True,charges=999,heal_self=False):
        super().__init__(name=name, active_n0=active_n0)
        self.charges = charges
        self.heal_self = heal_self

    def doNightAction(self,game=None,owner=None):
        super().doNightAction(game=game,owner=owner)
        if(self.charges > 0):
            if(not self.heal_self):
                targetable_players = [x for x in game.alive_players if x != owner]
            else:
                targetable_players = [x for x in game.alive_players]    
            target = game.chooseRandPlayer(targetable_players)
            game.addNightAction(Action(action_type=ActionType.HEAL, target=target, owner=owner))
            self.charges-=1

    def claim(self,game=None, owner=None):
        super().claim(game=game, owner=owner)
        return (self,owner.results)