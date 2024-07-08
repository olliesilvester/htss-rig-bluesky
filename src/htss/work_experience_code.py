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
from htss.data_access import get_client, print_docs  # noqa: F401
from htss.devices import beam, det, sample
from htss.plans.exercise import exercise_scan

RE = RunEngine()
with DeviceCollector():
    sam = sample()
    detector = det()
    be = beam()
print("All devices connected")

# bec = BestEffortCallback()
# RE.subscribe(bec)

tiled = get_client()
tiled.login(username="htss")

RE.subscribe(tiled.post_document)
devices.suppress_epics_warnings()
RE(bps.rd(be.power))
RE(bps.mv(sam.theta, 300))


def disarm():
    yield from bps.unstage(detector)


# RE(exercise_scan(detector, sam))
# print("scan done")


ds = tiled[-1]
ds["det_image"][0].plot()
plt.show()
