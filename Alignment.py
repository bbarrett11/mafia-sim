import re
from math import ceil
from Action import Action, ActionType

class Alignment:
    def __init__(self, name: str = "",win_con: str = "", night_action = None):
        if(name == "" or win_con == ""):
            raise Exception("Invalid Alignment")
        self.name = name
        self.win_con = win_con
        self.night_action = night_action
        self.game = None
        
    def checkWinCon(self) -> bool:
        num_same = self.game.countAlignment(alignment=self)
        # print(f"{self.name}same: {num_same}")
        if(re.match("last faction standing",self.win_con, re.IGNORECASE)):
            return num_same == len(self.game.alive_players)
        elif(re.match("parity",self.win_con, re.IGNORECASE)):
            return num_same >= ceil(len(self.game.alive_players)/2.0)

    def doNightAction(self):
        if(re.match("2[\s]*kp till 2",self.night_action, re.IGNORECASE)):
            # 2 kp
            if(self.game.countAlignment(alignment=self) > 2):
                # Sometimes double stack for now
                for i in range(2):
                    rand_town = self.game.chooseRandPlayer([x for x in self.game.alive_players if not x.alignment.name == self.name])
                    self.game.addNightAction(Action(action_type=ActionType.KP,target=rand_town))
            else:
                rand_town = self.game.chooseRandPlayer([x for x in self.game.alive_players if not x.alignment.name == self.name])
                self.game.addNightAction(Action(action_type=ActionType.KP,target=rand_town))

        elif(re.match("2[\s]*kp",self.night_action, re.IGNORECASE)):
            # 2 kp
            for i in range(2):
                rand_town = self.game.chooseRandPlayer([x for x in self.game.alive_players if not x.alignment.name == self.name])
                self.game.addNightAction(Action(action_type=ActionType.KP,target=rand_town))
    
    def __str__(self):
        return self.name
    
    def __eq__(self, other):
        return self.name == other.name