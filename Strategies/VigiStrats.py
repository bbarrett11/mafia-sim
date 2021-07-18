from Strategy import Strategy

# Activate on certain provided night phases, target random other player
class VigiStratSimpleActivation(Strategy):
    def __init__(self,name="",description="",when_to_activate : [str] = []):
        super().__init__(name,description)
        self.when_to_activate = when_to_activate
        
    def doIClaim(self,gamestate=None) -> bool:
        super().doIClaim(gamestate)
        # always claim
        return True
    def doIActivate(self,gamestate=None) -> bool:
        super().doIActivate(gamestate)
        # claim only certain nights
        return gamestate.phase in self.when_to_activate
    def whoDoITarget(self, gamestate=None):
        super().whoDoITarget(gamestate)
        # random target
        targetable_players = [x for x in gamestate.alive_players 
                              if x != self.role.owner]
        target = gamestate.chooseRandPlayer(targetable_players)
        return target

# Wait for someone to be red-checked until given night.
# Target is chosen from unconfirmed other players
class VigiStratSmartActivation(Strategy):
    def __init__(self,name="",description="",when_to_activate : [str] = []):
        super().__init__(name,description)
        self.when_to_activate = when_to_activate
        
    def doIClaim(self,gamestate=None) -> bool:
        super().doIClaim(gamestate)
        # always claim
        return True
    def doIActivate(self,gamestate=None) -> bool:
        super().doIActivate(gamestate)
        # activate only certain nights or if confirmed mafia is alive
        return gamestate.phase in self.when_to_activate or len(set(gamestate.alive_players).intersection(gamestate.believed_mafia)) > 0
    def whoDoITarget(self, gamestate=None):
        super().whoDoITarget(gamestate)
        # mafia targets
        mafia_targets = set(gamestate.alive_players).intersection(gamestate.believed_mafia)
        if(len(mafia_targets) > 0):
            targetable_players = list(mafia_targets)
        else:
            # random unconfirmed target
            targetable_players = [x for x in gamestate.alive_players 
                              if x != self.role.owner and 
                                 x not in gamestate.believed_town]
        target = gamestate.chooseRandPlayer(targetable_players)
        return target



