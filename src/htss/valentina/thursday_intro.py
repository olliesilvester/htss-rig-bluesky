from htss import run_plans_here
from htss.devices import BackLightPower
from htss.run_plans_here import be
import time
from ophyd.sim import det1

def plan1():
    be.power = BackLightPower.ON
    be.power = BackLightPower.OFF
    time.sleep(5)
    be.power = BackLightPower.ON

