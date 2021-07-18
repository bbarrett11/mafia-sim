from Alignment import Alignment

from Role import Role
from Roles.Medic import Medic
from Roles.Vigi import Vigi
from Roles.Cop import Cop
from Roles.Smart_Hunter_Ven import Smart_Hunter_Ven
from Roles.Innocent_Child import Innocent_Child
from Roles.Possum import Possum

import Strategy
from Strategies.VigiStrats import VigiStratSimpleActivation
from Strategies.VigiStrats import VigiStratSmartActivation

ALIGNMENT_TOWN       = Alignment(name="Town",win_con="Last Faction Standing",night_action="None")
ALIGNMENT_MAFIA_2KP2 = Alignment(name="Mafia",win_con="Parity", night_action="2 kp till 2")
ALIGNMENT_MAFIA      = Alignment(name="Mafia",win_con="Parity", night_action="1 kp")

MEDIC           = Medic(name="Medic",active_n0=True,heal_self=False)
ONESHOTVIGI     = Vigi(name="One Shot Vigi",active_n0=True,charges=1)
ONESHOTVIGINON0 = Vigi(name="One Shot Vigi",active_n0=False,charges=1)

COP              = Cop(name="Full Alignment Cop",active_n0=True,target_self=False)
SMART_HUNTER_VEN = Smart_Hunter_Ven(name="Smart Hunter")
INNOCENT_CHILD   = Innocent_Child(name="Inno Child")
POSSUM           = Possum(name="Possum")

VANILLA_TOWN     = Role(name="Vanilla Town", active_n0=False)
MAFIA_GOON       = Role(name="Mafia Goon", active_n0=False)

STRATEGY_DEFAULT    = Strategy.DefaultStrategy(name="Default Strategy",description="Target random, always activate and claim")
STRATEGY_ACTIVATEN1 = VigiStratSimpleActivation(name="Simple Activation",description="Activate on certain nights",when_to_activate = ["n1"])
STRAT_SMARTVIGIN2 = VigiStratSmartActivation(name="Smart Activation",description="Activate if known mafia or if deadline reached",when_to_activate = [])

