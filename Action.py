from enum import Enum

class ActionType(Enum):
    HEAL = 0
    KP = 1
    CHECK = 2
    INFO = 3

class Action:
    def __init__(self, action_type=None, target=None, owner=None, log=None):
        if(action_type == None):
            raise Exception("Action is type NONE")
        targeted_actions = [ActionType.CHECK,
                            ActionType.HEAL,
                            ActionType.KP,
                            ]
        if(action_type in targeted_actions  and target == None):
            raise Exception("Action not targetting anyone")
        
        self.type = action_type
        self.target = target
        self.owner = owner
        self.log = log
        

    def __str__(self):
        if(self.target):
            return f"{self.owner} uses {self.type} targeting {self.target.name}"
        elif(self.type == ActionType.INFO):
            return str(self.type) + ": " + self.log
            
        