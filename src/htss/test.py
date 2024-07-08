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

devices.suppress_epics_warnings()


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



def read_things():
    x = yield from bps.rd(sam.x)
    theta = yield from bps.rd(sam.theta)
    print(theta)
    yield from bps.mv(sam.theta, 180)
    theta = yield from bps.rd(sam.theta)
    print(theta)

bec = BestEffortCallback()
RE.subscribe(bec)
RE.waiting_hook = ProgressBarManager()
#RE(bps.mv(be.power, BacklightPower.ON))
RE(read_things())
#RE(exercise_scan(detector, sam))


