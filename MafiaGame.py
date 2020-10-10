import copy as cp
import random as rand
import Constants
import re

import logging
logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger('matplotlib.font_manager').disabled = True

from Action import Action, ActionType
from Player import Player

class MafiaGame:
    def __init__(self, setup = None):
        self.setup = setup
        self.alive_players = cp.deepcopy(setup.players)
        self.believed_town = []
        self.believed_mafia = []
        self.dead_players = []
        self.game_over = False
        self.alignments = setup.teams
        self.winner = None
        self.alignment_numbers_history = []

        # Setup players and roles
        for player in self.alive_players + self.dead_players:
            player.game = self
            player.role.owner = player
            player.role.game = self
        for alignment in self.alignments:
            alignment.game = self

    def cleanup(self):
        for player in self.alive_players + self.dead_players:
            player.game = None
            player.role.owner = None
            player.role.game = None
        for alignment in self.alignments:
            alignment.game = None

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
        
        # prevents copy recursion
        self.cleanup()
    
    def addNightAction(self,action=None):
        if(action == None):
            raise Exception("Action is none")
        self.night_actions.append(action)
        
    def doNightPhase(self):
        for alignment in self.alignments:
            alignment.doNightAction()
        for player in self.alive_players:
            player.doNightAction()
        self.resolveNightActions()
    
    def resolveNightActions(self):
        for action in self.night_actions:
            logger.debug(str(action))
        # Check actions
        for action in [x for x in self.night_actions if x.type == ActionType.CHECK]:
            action.owner.results.append((action.target,action.target.alignment))
            logger.debug("Checked "+action.target.name)
            logger.debug(str(action.owner.results))

        # Heal actions
        for action in [x for x in self.night_actions if x.type == ActionType.HEAL]:
            otherKPtargets = [y for y in self.night_actions if y.target == action.target and y.type == ActionType.KP]
            if(len(otherKPtargets) > 0):
                self.night_actions.remove(otherKPtargets[0])
                logger.debug("Healed! "+action.target.name)
        
        # KP actions
        for action in [x for x in self.night_actions if x.type == ActionType.KP]:
            if(action.target in self.alive_players):
                self.exile(action.target)
                logger.debug("KP: "+action.target.name)
        logger.debug("")

    def doDayPhase(self):
        rngs = rand.randint(0,2)+1 # RNG plus guaranteed
        while(rngs > 0):
            # Chance to formal mafia
            base = len([x for x in self.alive_players if x.alignment.name == Constants.ALIGNMENT_MAFIA.name])/len(self.alive_players)
            if(rand.random() < base):
                exile_list = [x for x in self.alive_players if x.alignment.name == Constants.ALIGNMENT_MAFIA.name]
            else:
                exile_list = [x for x in self.alive_players if x.alignment.name == Constants.ALIGNMENT_TOWN.name]
            town_exile=self.chooseRandPlayer(players=exile_list)
            logger.debug("Town formal "+town_exile.name)
            exiled = self.formal(town_exile)
            rngs -= 1
            if(exiled):
                break
    
    def formal(self,player: Player) -> bool:
            claim = player.claimInFormal()
            role_claim = "None"
            if(claim['role']):
                role_claim = str(claim['role']['role']) + " "+str([f"{p}, {al}" for p, al in claim['role']['results']])
            logger.debug(player.name+ " claims "+str(claim['alignment'])+" "+role_claim)
            # Exile claimed Mafia duh
            if(claim['alignment'] == Constants.ALIGNMENT_MAFIA):
                logger.debug("Town exile "+player.name)
                self.exile(player)
                return True
            elif(claim['role'] == None):
                logger.debug("Town exile "+player.name)
                self.exile(player)
                return True
            # Don't exile town PRs if believed
            else:
                logger.debug("Town do not exile "+player.name)                
                return False

    def exile(self, player:Player):
        if(player == None):
            return
        self.alive_players.remove(player)
        self.dead_players.append(player)
        
    def chooseRandPlayer(self,players=None) -> Player:
        # TODO different strategies based on alignment
        if(players == None):
            return None
        indx = rand.randint(0,len(players)-1)
        # print("Choose"+str(indx))
        return players[indx]
        
    def checkGame(self) -> int:
        game_end = 0
        for alignment in self.alignments:
            if(alignment.checkWinCon()):
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
                
    def countAlignment(self, alignment=None) -> int:
        if(not alignment):
            raise Exception("Counting alignment of None")
        num_same=0
        for player in self.alive_players:
            if player.alignment.name == alignment.name:
                num_same+=1
        return num_same
        