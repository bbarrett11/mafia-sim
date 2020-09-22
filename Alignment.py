import re
from math import ceil
from Action import Action, ActionType

class Alignment:
    def __init__(self, name="",win_con="", night_action=None):
        if(name == "" or win_con == ""):
            raise Exception("Invalid Alignment")
        self.name = name
        self.win_con = win_con
        self.night_action = night_action

    def checkWinCon(self, game=None):
        num_same = game.countAlignment(alignment=self)
        # print(f"{self.name}same: {num_same}")
        if(re.match("last faction standing",self.win_con, re.IGNORECASE)):
            return num_same == len(game.alive_players)
        elif(re.match("parity",self.win_con, re.IGNORECASE)):
            return num_same >= ceil(len(game.alive_players)/2.0)

    def doNightAction(self,game=None):
        if(re.match("2[\s]*kp till 2",self.night_action, re.IGNORECASE)):
            # 2 kp
            if(game.countAlignment(alignment=self) > 2):
                # Sometimes double stack for now
                for i in range(2):
                    rand_town = game.chooseRandPlayer([x for x in game.alive_players if not x.alignment.name == self.name])
                    game.addNightAction(Action(action_type=ActionType.KP,target=rand_town))
            else:
                rand_town = game.chooseRandPlayer([x for x in game.alive_players if not x.alignment.name == self.name])
                game.addNightAction(Action(action_type=ActionType.KP,target=rand_town))

        elif(re.match("2[\s]*kp",self.night_action, re.IGNORECASE)):
            # 2 kp
            for i in range(2):
                rand_town = game.chooseRandPlayer([x for x in game.alive_players if not x.alignment.name == self.name])
                game.addNightAction(Action(action_type=ActionType.KP,target=rand_town))
    def __str__(self):
        return self.name