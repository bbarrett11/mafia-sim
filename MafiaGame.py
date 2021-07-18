import copy as cp
import random as rand
import re

import logging
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger('matplotlib.font_manager').disabled = True

from Action import Action, ActionType
from Player import Player

class MafiaGame:
    def __init__(self, setup = None, verbose = False):
        if(setup== None):
            raise Exception("Game has no setup")
        
        if(verbose):
            logging.getLogger().setLevel(logging.DEBUG)

        self.setup = setup
        self.alive_players : [Player] = cp.deepcopy(setup.players)
        self.hidden_players = [] # For possum role
        self.believed_town = []
        self.believed_mafia = []
        self.dead_players = []
        self.game_over = False
        self.alignments = setup.teams
        self.winner = None
        self.alignment_numbers_history = []
        self.night_actions = []
        # Factor that determines town's skill at finding mafia
        self.town_skill_mod = 1.0
        self.day_start = setup.day_start
        # Percentage time town believe claim during formal
        self.believe_claim = 1.0
        # Percentage time town is willing to lose to claim
        self.lose_to_claim = 1.0
        # Percentage time mafia fake claim
        self.fake_claim_percent = 0.0
        
        # Setup players and roles
        for player in self.alive_players:
            player.game = self
            player.role.owner = player
            player.role.game = self
        for alignment in self.alignments:
            alignment.game = self
        
    def cleanup(self) -> None:
        # cleanup references in player and alignment objects
        for player in self.alive_players:
            player.game = None
            player.role.owner = None
            player.role.game = None
        for alignment in self.alignments:
            alignment.game = None

    def play(self) -> None:
        day = 0
        # print("Playing game " + str([str(x) for x in self.alive_players]))
        # Main Day/Night Loop
        while(not self.game_over):
            # Night phase
            if(not self.day_start):
                self.phase = f"n{day}"
                self.doNightPhase(day=day)

            if(self.checkGame() == 1):
                break
            day+=1
            # Day phase
            self.phase = f"d{day}"
            self.doDayPhase()
            if(self.checkGame() == 1):
                break
        
        # prevents copy recursion
        self.cleanup()
    
    def addNightAction(self,action=None) -> None:
        if(action == None):
            raise Exception("Action is none")
        self.night_actions.append(action)
        
    def doNightPhase(self, day=-1) -> None:
        for alignment in self.alignments:
            alignment.doNightAction()
        
        for player in (self.alive_players+self.hidden_players):
            if(player.role.active_n0 or not day == 0):
                player.doNightAction()
        self.resolveNightActions()
    
    def resolveNightActions(self) -> None:
        for action in self.night_actions:
            logger.debug(str(action))
        # Check actions
        for action in [x for x in self.night_actions if x.type == ActionType.CHECK]:
            action.owner.results.append({"type":ActionType.CHECK,"content":(action.target,action.target.alignment)})
            logger.debug("Checked "+action.target.name)
            logger.debug(str(action.owner.results))
            self.night_actions.remove(action)

        # Heal actions
        for action in [x for x in self.night_actions if x.type == ActionType.HEAL]:
            otherKPtargets = [y for y in self.night_actions if y.target == action.target and y.type == ActionType.KP]
            if(len(otherKPtargets) > 0):
                self.night_actions.remove(otherKPtargets[0])
                logger.debug("Healed! "+action.target.name)
            self.night_actions.remove(action)

        
        # KP actions
        for action in [x for x in self.night_actions if x.type == ActionType.KP]:
            if(action.target in (self.alive_players+self.hidden_players)):
                self.exile(action.target)
                logger.debug("KP: "+action.target.name)
            self.night_actions.remove(action)

        logger.debug("")

        # INFO actions
        for action in [x for x in self.night_actions if x.type == ActionType.INFO]:
            logger.debug("INFO: "+action.log)
            self.night_actions.remove(action)

        logger.debug("")

        # Clear night actions
        self.night_actions = []

    def doDayPhase(self) -> None:
        # count players at start of day for logging
        numbers = []
        for i, team in enumerate(self.alignments):
            numbers.append(len([x for x in self.alive_players if x.alignment == team]))
        self.alignment_numbers_history.append(numbers)
        logger.debug(f"{self.phase} has {len(self.alive_players)} alive {[str(p) for p in self.alive_players]}")
        # Sleep strat
        if(len(self.alive_players) == 4 or len(self.alive_players) == 6 ):
            return

        rngs = rand.randint(0,2)+1 # RNGs plus 1 guaranteed
        while(rngs > 0):
            town_exile=self.getTownExile()
            # Chance to formal mafia
            logger.debug("Town formal "+town_exile.name)
            exiled = self.formal(town_exile)
            rngs -= 1
            if(exiled):
                break
            elif(rngs == 0):
                logger.debug(f"Town Sleep")

    def getTownExile(self) -> Player:
        # If have a believed mafia, get them first
        for player in self.believed_mafia:
            if(player in self.alive_players):
                return player
        # Don't lynch green checks
        considered_players = [x for x in self.alive_players if x not in self.believed_town]
        if(len(considered_players) == 0):
            logger.debug(f"Something is very wrong since everyone is \"Confirmed\"")
            raise Exception("The game should be over but it is not everyone is \"Confirmed\"")
        # otherwise "true" random over alive players
        mafia_rate = self.town_skill_mod*self.countAlignment(self.setup.mafia_type)
        total_rate = len(considered_players)-self.countAlignment(self.setup.mafia_type)+mafia_rate
        mafia_find_rate = mafia_rate/float(total_rate)
        if(rand.random() < mafia_find_rate):
            exile_list = [x for x in considered_players if x.alignment == self.setup.mafia_type]
        else:
            exile_list = [x for x in considered_players if x.alignment == self.setup.town_type]
        town_exile = self.chooseRandPlayer(players=exile_list)
        return town_exile
    
    def formal(self,player: Player) -> bool:
            claim = player.claimInFormal()
            role_claim = "None"
            if(claim['role']):
                role_claim = str(claim['role']['role']) + " "+str([f"{c['content'][0]}, {c['content'][1]}" for c in claim['role']['results']])
            logger.debug(player.name+ " claims "+str(claim['alignment'])+" "+role_claim)
            # Exile claimed Mafia duh
            if(claim['alignment'] == self.setup.mafia_type):
                logger.debug("Town exile "+player.name)
                self.exile(player)
                return True
            elif(claim['role'] == None):
                logger.debug("Town exile "+player.name)
                self.exile(player)
                return True
            # Don't exile town PRs if believed
            else:
                # Believe Claim
                if (rand.random() < self.believe_claim):
                    if (rand.random() < self.lose_to_claim):
                        self.confirmTown(player)
                        for x in claim['role']['results']:
                            if x['type'] == ActionType.CHECK:
                                p, a = x['content']
                                if(a == self.setup.town_type):
                                    self.confirmTown(p)
                                else:
                                    self.confirmMafia(p)
                    logger.debug("Town do not exile "+player.name)                
                    return False
                #Don't Believe and lynch
                else:
                    return True

    def exile(self, player: Player) -> None:
        if(player == None):
            return
        if(player.role.has_exile_action):
            logger.debug("Exile Action occurs")
            player.role.doExileAction()
        logger.debug(f"{player} has died")
        if(player in self.alive_players):
            self.alive_players.remove(player)
        elif(player in self.hidden_players):
            self.hidden_players.remove(player)
        else:
            raise Exception("Player is not alive so can't be exiled")
        self.dead_players.append(player)
 
    def confirmTown(self, player: Player) -> None:
        if(player == None):
            raise Exception("Player being confirmed is none")
        logger.debug(f"{player} is confirmed town")
        self.believed_town.append(player)

    def confirmMafia(self, player: Player) -> None:
        if(player == None):
            raise Exception("Player being confirmed is none")
        logger.debug(f"{player} is confirmed MAFIA")
        self.believed_mafia.append(player)

    def chooseRandPlayer(self,players=None) -> Player:
        if(players == None):
            return None
        return rand.choice(players)
  
    def getAliveTeam(self,player=None) -> [Player]:
        if(not player):
            raise Exception("Player is None")
        pl_list = [x for x in self.alive_players if x.alignment == player.alignment]
        return pl_list

    def checkGame(self) -> int:
        game_end = 0
        for alignment in self.alignments:
            if(alignment.checkWinCon()):
                self.game_over = True
                self.winner = alignment
                logger.debug(f"{self.winner} has won\n")
                return 1
        return 0
    
    def checkDayNight(self,day=0) -> bool:
        return re.match(f"[dn]{day}",self.phase)            
    
    def countAlignment(self, alignment=None) -> int:
        if(not alignment):
            raise Exception("Counting alignment of None")
        num_same=0
        for player in self.alive_players:
            if player.alignment.name == alignment.name:
                num_same+=1
        return num_same
        