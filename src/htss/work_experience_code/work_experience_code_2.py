import asyncio
import os
from time import sleep

import bluesky.plan_stubs as bps
import epicscorelibs.path.pyepics
import matplotlib.pyplot as plt
from bluesky import RunEngine
from bluesky.callbacks.best_effort import BestEffortCallback
from bluesky.preprocessors import contingency_wrapper
from dodal.utils import make_all_devices
from ophyd_async.core import Device, DeviceCollector
from ophyd_async.epics.motion import Motor
import htss.devices as devices
from htss.__main__ import main
from htss.devices import beam, det, sample
from htss.plans.exercise import exercise_scan
from htss.devices import BacklightPower
from databroker import Broker
from bluesky.utils import ProgressBarManager
from time import sleep

devices.suppress_epics_warnings()

"""Short introduction to bluesky plan stubs and device connection. See how to read values from devices and to set values"""


#Start instance of the RunEngine
RE = RunEngine()

#Create and connect to the devices
with DeviceCollector():
    sam = sample()
    detector = det()
    be = beam()
print("All devices connected")

def print_motor_states():
    x = yield from bps.rd(sam.x)
    theta = yield from bps.rd(sam.theta)
    print(f"Motor X is currently as position {x}, and theta is at {theta}")

def turn_light_on_and_off():
    print("Turning light off")
    yield from bps.mv(be.power, BacklightPower.OFF)
    sleep(2)
    print("Turning light back on")
    yield from bps.mv(be.power, BacklightPower.ON)

bec = BestEffortCallback()
RE.subscribe(bec)
RE.waiting_hook = ProgressBarManager()
#RE(bps.mv(be.power, BacklightPower.ON))
RE(exercise_scan(detector, sam))


