from Role import Role
from Action import ActionType, Action
import random
class Innocent_Child(Role):
    # Normal medic: cannot save themself
    def __init__(self, name=''):
        super().__init__(name=name)
        self.confirmed = False
        
    def doNightAction(self):
        super().doNightAction()
        if(not self.confirmed):
            if(random.random() < 1):
                self.game.confirmTown(self.owner)
                self.confirmed = True

    def claim(self):
        super().claim()
        return {"role": self,"results": self.owner.results}