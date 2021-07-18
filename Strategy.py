

class Strategy:
    def __init__(self,name="",description=""):
        self.name = name
        self.description = description
        self.role = None

    def doIClaim(self,phase="",gamestate=None) -> bool:
        if(gamestate == None):
            raise Exception("Issue with reasoning about claiming")
        pass
    def doIActivate(self,gamestate=None) -> bool:
        if(gamestate == None):
            raise Exception("Issue with reasoning about activation")
    def whoDoITarget(self, gamestate=None):
        if(gamestate == None):
            raise Exception("Issue with reasoning about who to target")
        pass
    
    def __str__(self):
        return str(name)

# Always claim, always activate if possible, target random player that isn't themself
class DefaultStrategy(Strategy):
    def __init__(self,name="",description=""):
        super().__init__(name,description)
        
    def doIClaim(self,gamestate=None) -> bool:
        super().doIClaim(gamestate)
        # always claim
        return True
    def doIActivate(self,gamestate=None) -> bool:
        super().doIActivate(gamestate)
        # always activate
        return True
    def whoDoITarget(self, gamestate=None):
        super().whoDoITarget(gamestate)
        # random target
        targetable_players = [x for x in gamestate.alive_players if x != self.role.owner]
        target = gamestate.chooseRandPlayer(targetable_players)
        return target
