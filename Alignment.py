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
        self.w_PR = 1
        self.w_confirmed_town = 1
        
    def checkWinCon(self) -> bool:
        num_same = self.game.countAlignment(alignment=self)
        # print(f"{self.name}same: {num_same}")
        if(re.match("last faction standing",self.win_con, re.IGNORECASE)):
            return num_same == len(self.game.alive_players)
        elif(re.match("parity",self.win_con, re.IGNORECASE)):
            return num_same >= ceil(len(self.game.alive_players)/2.0)

    def addKP(self):
        town_players = [x for x in self.game.alive_players if not x.alignment == self]
        for player in self.game.believed_town:
            if(player in self.game.alive_players):
                town_players = [player]
        rand_town = self.game.chooseRandPlayer(town_players)
        self.game.addNightAction(Action(action_type=ActionType.KP,target=rand_town))

    def doNightAction(self):
        if(re.match("2[\s]*kp till 2",self.night_action, re.IGNORECASE)):
            # 2 kp
            if(self.game.countAlignment(alignment=self) > 2):
                # Sometimes double stack for now
                for i in range(2):
                    self.addKP()
            else:
                self.addKP()

        elif(re.match("2[\s]*kp",self.night_action, re.IGNORECASE)):
            # 2 kp
            for i in range(2):
                self.addKP()
        elif(re.match("1[\s]*kp",self.night_action, re.IGNORECASE)):
            # 1 kp
            self.addKP()


    def __str__(self):
        return self.name
    
    def __eq__(self, other):
        if(not other or not other.name):
            return False

        return self.name == other.name