import time

from htss import run_plans_here
from htss.devices import BacklightPower
from htss.run_plans_here import be
from htss.run_plans_here import detector, sam
from bluesky.plans import count, scan
import bluesky.plan_stubs as bps
from htss.run_plans_here import RE
from ophyd_async.epics.motion import Motor

dets = [detector]

#intro 

def turn_light_on_and_off():
    yield from bps.abs_set(be.power, BacklightPower.OFF, wait=True)
    time.sleep(5)
    yield from bps.abs_set(be.power, BacklightPower.ON, wait=True)

def count_detector():
    yield from count(dets, num=1)

def move_motor_x(value):
    yield from bps.mv(sam.x, value)

def move_motor_a(value):
    yield from bps.mv(sam.theta, value)

#part one

def light_on():
    yield from bps.abs_set(be.power, BacklightPower.ON, wait=True)

def move_a_zero():
    yield from bps.mv(scan(dets, sam.theta, 0))

def takes_five_images():
    yield from scan(dets, sam.theta, 0, 80, num = 5)

def light_off():
    yield from bps.abs_set(be.power, BacklightPower.OFF, wait=True)


def combined():
    yield from bps.abs_set(be.power, BacklightPower.ON, wait=True)
    yield from bps.mv(sam.theta, 0)
    yield from scan(dets, sam.theta, 0, 80, num = 5)
    yield from bps.abs_set(be.power, BacklightPower.OFF, wait=True)


#RE(combined())

#part two
class parameter_outside_limits(Exception):
    pass


async def set(self, x_pos: float, y_pos: float):
    val = await Motor.low_limit_travel.get_value()
    val2 = await Motor.high_limit_travel.get_value()
    if val < Motor.low_limit_travel or val2 > Motor.high_limit_travel:
        raise parameter_outside_limits
    
