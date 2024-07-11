from htss.devices import SampleStage
import pytest
from htss.devices import PositionOutOfRange
from htss.devices import BacklightPower, SampleStage, beam, det, sample
from ophyd_async.core import Device, DeviceCollector
import asyncio
from htss.devices import _calculate_expected_time
from htss.run_plans_here import RE
from unittest.mock import MagicMock, patch, AsyncMock

with DeviceCollector(mock=True):
    sam = sample()
    detector = det()
    be = beam()


def test_if_position_not_within_limits_exception_raised():
    with pytest.raises(PositionOutOfRange, match="Position entered out of range."):
        _calculate_expected_time(-150, 0, 30, 365, 0, 20, 100, 0)

def test_if_within_limits_no_exception_raised():
    _calculate_expected_time(3,5,6,5,2,6,10,0)
    

def test_given_distance_and_velocity_then_calculated_time_is_correct():
    assert _calculate_expected_time(3,5,6,5,2,6,10,0) == 0.5
    


async def test_set_is_called_with_correct_arguments():
    #we want this test to confirm that after calling the set on sample stage, the set functions are calld on samplestage.x and samplestage.theta with the correct arguments
    with patch("htss.devices._calculate_expected_time", return_value=10):
        sam.x.set = AsyncMock()
        sam.theta.set = AsyncMock()

        await sam.set(15,60)

        sam.x.set.assert_called_with(15,15)
        sam.theta.set.assert_called_with(60,15)
        


    
    

async def test_after_using_set_then_previous_positions_are_correct():
    assert sam.previous_positions == [[],[]]
    with patch ("htss.devices._calculate_expected_time", return_value = 10):
        sam.x.set = AsyncMock(return_value=0)
        sam.theta.set = AsyncMock(return_value=0)
        await sam.set(0,3)
        await sam.set(3,4)
        await sam.set(5,6)
        assert sam.previous_positions == [[0,3,5],[3,4,6]]
    

async def test_read_gives_correct_values():
    with patch ("htss.devices.get_value", return_value=10):
        assert await sam.read() == {"X": 10, "A": 5}


asyncio.run(test_read_gives_correct_values())