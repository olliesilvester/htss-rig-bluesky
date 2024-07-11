import time

from htss import run_plans_here
from htss.devices import BacklightPower
from htss.run_plans_here import be
from htss.run_plans_here import det
from bluesky.plans import count
import bluesky.plan_stubs as bps
from htss.run_plans_here import RE

#intro 

def turn_light_on_and_off():
    yield from bps.abs_set(be.power, BacklightPower.ON, wait=True)
    time.sleep(5)
    be.power = BacklightPower.ON

def count_detector():
    yield from count(det, num=1)

def move_motor_x():
    yield from bps.mv(scan(det, move_motor_x, 1))

def move_motor_a():
    yield from bps.mv(scan(det, move_motor_a, 1))

#part one

def light_on():
    yield from bps.abs_set(be.power, BacklightPower.ON, wait=True)

def move_a_zero():
    yield from bps.mv(scan(det, move_motor_a, 0))

def takes_five_images():
    for i in range(5):
        yield from scan(det, num = 1)

def light_off():
    yield from bps.abs_set(be.power, BacklightPower.OFF, wait=True)