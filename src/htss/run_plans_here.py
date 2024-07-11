import asyncio
import os
import subprocess
from enum import Enum
from time import sleep

import bluesky.plan_stubs as bps
import epicscorelibs.path.pyepics
import matplotlib.pyplot as plt
from bluesky import RunEngine
from bluesky.callbacks.best_effort import BestEffortCallback
from bluesky.plans import count, scan
from bluesky.preprocessors import contingency_wrapper
from bluesky.utils import ProgressBarManager
from databroker import Broker
from dodal.utils import make_all_devices
from ophyd_async.core import Device, DeviceCollector
from ophyd_async.epics.motion import Motor

import htss.devices as devices
from htss.__main__ import main
from htss.devices import BacklightPower, SampleStage, beam, det, sample
from htss.plans.exercise import exercise_scan

devices.suppress_epics_warnings()

# Start instance of the RunEngine
RE = RunEngine()
# Create and connect to the devices
with DeviceCollector():
    sam = sample()
    detector = det()
    be = beam()

print("All devices connected")
bec = BestEffortCallback()
RE.subscribe(bec)
RE.waiting_hook = ProgressBarManager()
dets = [detector]

"""Look at the devices we have access to in devices.py . In vscode, press ctrl+p and click devices to quickly find the file

We have the SampleStage which contains two motors - x (this one keeps breaking) and theta

We have a Backlight with a 'power' which we can turn on and off

We also have the detector which we can take images with. We can treat this in a similar way to the detector simulator from yesterday
"""

#introduction
async def light_on_and_off():
    yield bps.abs_set(be.power, BacklightPower.ON, wait=True)
    await asyncio.sleep(5)
    yield bps.abs_set(be.power, BacklightPower.OFF)


def trigger_detector():
    yield from count(dets)


def move_motor_x(position):
    yield from bps.mv(sam.x, position)


def move_omega(position):
    yield from bps.mv(sam.theta, position)

#thursday part 1

def light_on():
    yield bps.abs_set(be.power, BacklightPower.ON)

def light_off():
    yield bps.abs_set(be.power, BacklightPower.OFF)

def move_omega_to_zero():
    yield from bps.mv(sam.theta, 0)

def scan_five_images():
    yield from scan(dets, detector.theta, 0, 100, 5)

#thursday part 2
class PositionOutOfRange(Exception):
    pass

def set(pos_x, pos_theta):
    try: 
        if pos_x < 0 or pos_x > 1:
            raise PositionOutOfRange
        elif pos_theta < 0 or pos_theta > 360:
            raise PositionOutOfRange
    except:
            



