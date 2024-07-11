
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
import time
import asyncio

class PositionOutOfRange(Exception):
    pass

class BacklightPower(str, Enum):
    ON = "On"
    OFF = "Off"


def _calculate_expected_time(pos_x, current_x, velocity_x, pos_theta, current_theta, velocity_theta, high_limit, low_limit) -> float:
    time_x = abs((pos_x - current_x)/velocity_x)
    time_theta = abs((pos_theta - current_theta)/velocity_theta)

    if pos_x < low_limit or pos_x > high_limit:
        raise PositionOutOfRange("Position entered out of range.")
    
    if time_x > time_theta:
        estimated_time = time_x
    else:
        estimated_time = time_theta

    return estimated_time

class SampleStage(Device):
    def __init__(self, prefix: str, name: str):
        self.x = Motor(prefix + "X")
        self.theta = Motor(prefix + "A")
        self.previous_positions = [[],[]]
        super().__init__(name)
    
    @AsyncStatus.wrap
    async def set(self, pos_x: float, pos_theta: float):
        self.previous_positions[0].append(pos_x)
        self.previous_positions[1].append(pos_theta)

        high_limit_awaitable = self.x.high_limit_travel.get_value()
        low_limit_awaitable = self.x.high_limit_travel.get_value()
        current_x_awaitable = self.x.user_readback.get_value()
        current_theta_awaitable = self.theta.user_readback.get_value()
        velocity_x_awaitable  = self.x.velocity.get_value()
        velocity_theta_awaitable = self.theta.velocity.get_value()

        high_limit, low_limit, current_x, current_theta, velocity_x, velocity_theta = await asyncio.gather(high_limit_awaitable, low_limit_awaitable, current_x_awaitable, current_theta_awaitable, velocity_x_awaitable, velocity_theta_awaitable)

        estimated_time =_calculate_expected_time(pos_x, current_x, velocity_x, pos_theta, current_theta, velocity_theta, high_limit, low_limit) + 5

        move_x = self.x.set(pos_x, estimated_time)
        move_theta = self.theta.set(pos_theta, estimated_time)
        await asyncio.gather(move_x, move_theta)
    
    @AsyncStatus.wrap
    async def read(self):
        current_pos_x = await self.x.user_readback.get_value()
        current_pos_theta = await self.theta.user_readback.get_value()
        current_positions = {"X": None, "A": None}
        current_positions["X"] = current_pos_x
        current_positions["A"] = current_pos_theta
        return current_positions




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
