import Simulator, Alignment, Constants, MafiaGame, MafiaSetup, Player, Role

Players = []
# 12 VT
# 3 Mafia Goons
num_medics = 1
for i in range(num_medics):
    Players.append(Player.Player(name=f"Me{i}",alignment=Constants.ALIGNMENT_TOWN,role=Constants.TOWN_MEDIC))
num_vigis = 1
for i in range(num_vigis):
    Players.append(Player.Player(name=f"V{i}",alignment=Constants.ALIGNMENT_TOWN,role=Constants.TOWN_ONESHOTVIGI))

num_VT = 10
for i in range(num_VT):
    Players.append(Player.Player(name=f"VT{i}",alignment=Constants.ALIGNMENT_TOWN,role=Constants.VANILLA_TOWN))

num_maf = 3
for i in range(num_maf):
    Players.append(Player.Player(name=f"Ma{i}",alignment=Constants.ALIGNMENT_MAFIA,role=Constants.MAFIA_GOON))
    
setup = MafiaSetup.MafiaSetup(players=Players,teams=[Constants.ALIGNMENT_TOWN,Constants.ALIGNMENT_MAFIA])

simulator = Simulator.Simulator(setup=setup,num_iterations=1000)

simulator.run(graph=False)
