from htss.__main__ import main
import bluesky.plan_stubs as bps
from htss.devices import sample, det, beam
from bluesky import RunEngine
import asyncio
from ophyd_async.epics.motion import Motor
from time import sleep
import os
from ophyd_async.core import Device
from bluesky import RunEngine
from dodal.utils import make_all_devices
import htss.devices as devices
from ophyd_async.core import DeviceCollector

RE = RunEngine()

with DeviceCollector():
    sam = sample()
    detector = det()
    be = beam()
print("All devices connected")

devices.suppress_epics_warnings()
RE(bps.rd(be.power))
RE(bps.mv(sam.theta, 300))