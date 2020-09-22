import copy as cp
import random as rand
import Constants
import re
import logging
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
from Action import Action, ActionType

class MafiaGame:
    def __init__(self, setup=None):
        self.setup = setup
        self.alive_players = cp.deepcopy(setup.players)
        self.dead_players = []
        self.game_over = False
        self.alignments = setup.teams
        self.winner = None
        self.alignment_numbers_history = []

        
    def play(self):
        day = 0
        # print("Playing game " + str([str(x) for x in self.alive_players]))
        
        while(not self.game_over):
            # Night phase
            self.phase = f"n{day}"
            self.night_actions = []
            self.doNightPhase()
            if(self.checkGame() == 1):
                break
            # Day phase
            self.phase = f"d{day}"
            self.doDayPhase()
            if(self.checkGame() == 1):
                break
            day+=1
            # print(str([str(x) for x in self.alive_players]))

        #return self.winner.name
    
    def addNightAction(self,action=None):
        if(action == None):
            raise Exception("Action is none")
        self.night_actions.append(action)
        
    def doNightPhase(self):
        for alignment in self.alignments:
            alignment.doNightAction(game=self)
        for player in self.alive_players:
            player.doNightAction(game=self)
        self.resolveNightActions()
    
    def resolveNightActions(self):
        for action in self.night_actions:
            logger.debug(str(action))
        # Heal actions
        for action in [x for x in self.night_actions if x.type == ActionType.HEAL]:
            otherKPtargets = [y for y in self.night_actions if y.target == action.target and y.type == ActionType.KP]
            if(len(otherKPtargets) > 0):
                self.night_actions.remove(otherKPtargets[0])
                logger.debug("Heal! "+action.target.name)
        
        # KP actions
        for action in [x for x in self.night_actions if x.type == ActionType.KP]:
            if(action.target in self.alive_players):
                self.exile(action.target)
                logger.debug("Kill: "+action.target.name)
        logger.debug("")

    
    def doDayPhase(self):
        rngs = rand.randint(0,2)+1 # RNG plus guaranteed
        while(rngs > 0):
            town_exile=self.chooseRandPlayer(players=self.alive_players)
            logger.debug("Town formal "+town_exile.name)
            exiled = self.formal(town_exile)
            rngs -= 1
            if(exiled):
                break
    
    def formal(self,player):
            claim = player.claimInFormal(game=self)
            logger.debug(player.name+ " claims "+str(claim[0])+" "+str(claim[1]))
            if(claim[0].name == Constants.ALIGNMENT_MAFIA.name):
                logger.debug("Town exile "+player.name)
                self.exile(player)
                return True
            elif(claim[1] == None):
                logger.debug("Town exile "+player.name)
                self.exile(player)
                return True                
            else:    
                return False

    def exile(self, player):
        if(player == None):
            return
        self.alive_players.remove(player)
        self.dead_players.append(player)
        
    def chooseRandPlayer(self,players=None):
        # TODO different strategies based on alignment
        if(players == None):
            return None
        indx = rand.randint(0,len(players)-1)
        # print("Choose"+str(indx))
        return players[indx]
        
    def checkGame(self):
        game_end = 0
        for alignment in self.alignments:
            if(alignment.checkWinCon(self)):
                self.game_over = True
                self.winner = alignment
                game_end = 1
        # Add numbers to history if day
        if(re.match("n",self.phase)):
            numbers = []
            for i, team in enumerate(self.alignments):
                numbers.append(len([x for x in self.alive_players if x.alignment.name == team.name]))
            self.alignment_numbers_history.append(numbers)
        return game_end
                
    def countAlignment(self, alignment=None):
        if(alignment == None):
            raise Exception("Counting alignment of None")
        num_same=0
        for player in self.alive_players:
            if player.alignment.name == alignment.name:
                num_same+=1
        return num_same
        