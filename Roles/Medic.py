from Role import Role
from Action import ActionType, Action
class Medic(Role):
    # Normal medic: cannot save themself
    def __init__(self, name='', active_n0=True,charges=999,heal_self=False):
        super().__init__(name=name, active_n0=active_n0)
        self.charges = charges
        self.heal_self = heal_self

    def doNightAction(self,game=None,player_doing_action=None):
        super().doNightAction(game=game,
                              player_doing_action=player_doing_action)
        if(self.charges > 0):
            targetable_players = [x for x in game.alive_players]
            if(not self.heal_self):
                targetable_players = [x for x in game.alive_players if x != player_doing_action]
            game.addNightAction(Action(action_type=ActionType.HEAL,target=game.chooseRandPlayer(targetable_players)))
            self.charges-=1

    def claim(self,game=None):
        super().claim(game=game)
        return self