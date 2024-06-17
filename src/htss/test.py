from htss.__main__ import main
import importlib
import bluesky.plan_stubs as bps
importlib.import_module("htss.startup")
from htss.devices import sample
from bluesky import RunEngine

RE = RunEngine()
sample = sample()
RE(bps.rd(sample.x))


