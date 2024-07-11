
import epics
from bluesky.protocols import Status
from dodal.devices.areadetector import AdAravisDetector
from ophyd import Component, Device, EpicsSignalWithRBV
from ophyd_async.epics.motion import Motor
from .names import pv_prefix
from ophyd_async.core import Device
from ophyd_async.epics.areadetector.aravis import AravisDetector
from ophyd_async.core import StaticDirectoryProvider
from enum import Enum
from ophyd_async.core import StandardReadable, AsyncStatus
from ophyd_async.epics.signal import epics_signal_rw


class BacklightPower(str, Enum):
    ON = "On"
    OFF = "Off"


class SampleStage(Device):
    def __init__(self, prefix: str, name: str):
        self.x = Motor(prefix + "X")
        self.theta = Motor(prefix + "A")
        super().__init__(name)

    @AsyncStatus.wrap
    async def set(self, x_pos: float, y_pos: float):
        """This setter will turn the backlight on when we move it in to the beam and off
        when we move it out."""
        
        #await getting the limits

        #check limits

class Backlight(StandardReadable):
    """Simple device to trigger the pneumatic in/out."""

    def __init__(self, prefix: str, name: str = "") -> None:
        self.power = epics_signal_rw(BacklightPower, prefix + "State")
        super().__init__(name)
    @AsyncStatus.wrap
    async def set(self, position: BacklightPower):
        """This setter will turn the backlight on when we move it in to the beam and off
        when we move it out."""
        await self.power.set(position)


def sample(name: str = "sample_stage") -> SampleStage:
    """
    Create sample stage Ophyd device

    Args:
        name: Name for this device for reference in events.
            Defaults to "sample_stage".

    Returns:
        SampleStage: A new Ophyd Device
    """

    return SampleStage(name=name, prefix=f"{pv_prefix()}-MO-MAP-01:STAGE:")


def det(name: str = "det") -> AravisDetector:
    """
    Create detector stage Ophyd-Async device

    Args:
        name: Name for this device for reference in events.
            Defaults to "det".

    Returns:
        SampleStage: A new Ophyd Device
    """
    dir_prov = StaticDirectoryProvider("/exports/mybeamline/data")
    

    det = AravisDetector(name=name, prefix=f"{pv_prefix()}-EA-DET-01:", directory_provider=dir_prov, hdf_suffix="HDF5:", drv_suffix="DET:")
    #det.read_attrs += ["cam"]
    #det.cam.read_attrs += ["acquire_time", "acquire_period"]
    #det.hdf.write_path_template = "%Y"
    return det

def beam(name: str = "beam") -> Backlight:
    """
    Create an object to represent the beam

    Args:
        name: Name for this device for reference in events.
            Defaults to "beam".

    Backlight:
        SampleStage: A new Ophyd Device
    """

    return Backlight(name=name, prefix=f"{pv_prefix()}-EA-BEAM-01:")

async def connect_to_device(device: Device):
    await device.connect()


def suppress_epics_warnings() -> None:
    def handle_messages(text):
        ...

    epics.ca.replace_printf_handler(handle_messages)
