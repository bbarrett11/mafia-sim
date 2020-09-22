from Alignment import Alignment
from Role import Role
from Roles.Medic import Medic
from Roles.Vigi import Vigi
from Roles.Cop import Cop

ALIGNMENT_TOWN=Alignment(name="Town",win_con="Last Faction Standing",night_action="None")
ALIGNMENT_MAFIA=Alignment(name="Mafia",win_con="Parity", night_action="2 kp till 2")

TOWN_MEDIC = Medic(name="Medic",active_n0=True,heal_self=False)
TOWN_ONESHOTVIGI = Vigi(name="One Shot Vigi",active_n0=True,charges=1)
TOWN_COP = Cop(name="Full Alignment Cop",active_n0=True,target_self=False)

VANILLA_TOWN = Role(name="Vanilla Town", active_n0=False)

MAFIA_GOON = Role(name="Mafia Goon", active_n0=False)

