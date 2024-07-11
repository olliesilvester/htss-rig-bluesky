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
    #be = beam()

print("All devices connected")
bec = BestEffortCallback()
RE.subscribe(bec)
RE.waiting_hook = ProgressBarManager()

def my_test_plan():
    yield from bps.abs_set(sam, 15, 360)

RE(my_test_plan())

"""Look at the devices we have access to in devices.py . In vscode, press ctrl+p and click devices to quickly find the file

We have the SampleStage which contains two motors - x (this one keeps breaking) and theta

We have a Backlight with a 'power' which we can turn on and off

We also have the detector which we can take images with. We can treat this in a similar way to the detector simulator from yesterday
"""
