import Simulator, Alignment, Constants, MafiaGame, MafiaSetup, Player, Role
import yaml
import copy
import sys



def loadSetupFromFile(file_name: str = "allstars"):

    player_role_to_obj = {
        "medic":Constants.MEDIC,
        "cop":Constants.COP,
        "vigi":Constants.ONESHOTVIGI,
        "no n0 vigi":Constants.ONESHOTVIGINON0,
        "vt":Constants.VANILLA_TOWN,
        "goon":Constants.MAFIA_GOON,
        "smart hunter ven":Constants.SMART_HUNTER_VEN,
        "inno child":Constants.INNOCENT_CHILD,
        "possum" : Constants.POSSUM,
    }
    player_strat_to_obj = {
        "none" : Constants.STRATEGY_DEFAULT,
        "activate_n1":Constants.STRATEGY_ACTIVATEN1,
        "smart_n2":Constants.STRAT_SMARTVIGIN2
    }
    player_align_to_obj = {
        "town":Constants.ALIGNMENT_TOWN,
        "mafia 2kp2":Constants.ALIGNMENT_MAFIA_2KP2,
        "mafia 1kp":Constants.ALIGNMENT_MAFIA,
    }
    players = []
    alignments = []

    # Load setup from file
    with open(f"Setups/{file_name}.yaml") as file:
        game = yaml.load(file,Loader=yaml.FullLoader)
        print(f"Loading Setup: {game['name']}")
        player_count = game['player_count']
        player_list = game['players']
        day_start = game['day_start']
        mafia_type = game['mafia_type']
        mafia_align = player_align_to_obj[mafia_type]
        if(player_count != sum([x['player']['count'] for x in player_list])):
            raise Exception("Incorrect number of players in setup")
        for obj in player_list:
            player = obj['player']
            try:
                alignment = player_align_to_obj[player['alignment']]
                role = player_role_to_obj[player['role']]
                if('strat' in player):
                    strat = player_strat_to_obj[player['strat']]
                else:
                    strat = player_strat_to_obj["none"]
            except Exception as e:
                print(e)
                print(f"Issue loading alignment: {player['alignment']} or role: {player['role']}")
                exit(1)
            for i in range(player['count']):
                players.append(Player.Player(name=f"{str(role)} {i+1}",alignment=alignment,role=copy.deepcopy(role),strategy=copy.deepcopy(strat)))
        print(f"Loaded Setup: {game['name']}")
    setup = MafiaSetup.MafiaSetup(players=players,
                                  day_start=day_start, 
                                  mafia_type=mafia_align,
                                  town_type=Constants.ALIGNMENT_TOWN)
    return setup

import argparse

if __name__ == '__main__':
    # Arguments
    parser = argparse.ArgumentParser(description='Simulate a Mafia Game.')
    parser.add_argument("-n","--name", action='store',dest="name",default="allstars",help="Name of the setup to be simulated \"NAME\".yaml")
    parser.add_argument("-i","--iterations", action='store',dest="iters",default=1,type=int,help="Number of iterations")
    parser.add_argument("-v","--verbose", action='store_true',dest="verbose",default=False,help="Verbose Debugging")
    args = parser.parse_args()
    setup_name = args.name
    number_of_iters = int(args.iters)
    verbose = int(args.verbose)
    
    setup = loadSetupFromFile(file_name=f"{setup_name}")
    print(f"Simulating Setup for {number_of_iters} iterations")
    simulator = Simulator.Simulator(setup=setup,num_iterations=number_of_iters)
    simulator.run(graph=False,verbose=verbose)
