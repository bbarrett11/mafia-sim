from enum import Enum

class ActionType(Enum):
    HEAL = 0
    KP = 1
    CHECK = 2

class Action:
    def __init__(self, action_type=None, target=None):
        if(action_type == None):
            raise Exception("Action is type NONE")
        if(action_type in [ActionType.CHECK,ActionType.HEAL,ActionType.KP]  and target == None):
            raise Exception("Action not targetting anyone")
        
        self.type = action_type
        self.target = target

    def __str__(self):
        return str(self.type) + " targeting " + self.target.name
        