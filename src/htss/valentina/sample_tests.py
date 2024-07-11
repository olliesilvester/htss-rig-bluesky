from ophyd_async.core import DeviceCollector

from htss.devices import sample, det, beam, _calculate_estimated_time, ParameterOutsideLimits

import pytest

from unittest.mock import MagicMock, patch, AsyncMock

from htss.run_plans_here import RE

import asyncio

with DeviceCollector(mock=True):
    sam = sample()
    detector = det()
    be = beam()


def test_if_position_not_within_limits_and_exception_raised():
    with pytest.raises(ParameterOutsideLimits):
        _calculate_estimated_time(-150, 0, 200, 100, 50, 60 )


def test_if_position_within_limits_then_no_exception_raised():
    _calculate_estimated_time(90, 0, 200, 100, [50], 60 )

def test_given_distance_and_velocity_then_calculated_time_is_correct():
    assert _calculate_estimated_time(90, 0, 200, 100, [50], 60) ==1/6

async def test_set_is_called_with_correct_arguments():
        with patch("htss.devices._calculate_estimated_time", return_value = 10):
            sam.x.set = AsyncMock()
            sam.theta.set = AsyncMock()
            await sam.set(0, 0)
            sam.x.set.assert_called_with(0, timeout = 15)
            sam.theta.set.assert_called_with(0, timeout = 15)


def test_after_using_set_then_previous_positions_are_correct():
    assert sam.previous_positions == []
    _calculate_estimated_time(90, 0, 200, 100, [50], 60 )
    _calculate_estimated_time(90, 0, 200, 100, [50], 60 )
    _calculate_estimated_time(90, 0, 200, 100, [50], 60 )
    _calculate_estimated_time(90, 0, 200, 100, [50], 60 )
    assert sam.previous_positions == [100, 100, 100, 100]


def test_read_gives_correct_values():
    ...

#def test_our_mock():
 #   with patch("htss.devices._calculate_estimated_time") as mock_estimated_time:
  #      mock_estimated_time.return_value(15)
#
 #       mock_estimated_time.assert_called_with()

        #expected_dictionary = {"x": 100, "theta": }

#test_if_position_not_within_limits_and_exception_raised()
#test_if_position_within_limits_then_no_exception_raised()
#test_given_distance_and_velocity_then_calculated_time_is_correct()
#asyncio.run(test_set_is_called_with_correct_arguments())
test_after_using_set_then_previous_positions_are_correct()