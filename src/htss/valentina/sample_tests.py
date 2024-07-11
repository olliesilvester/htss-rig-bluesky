from ophyd_async.core import DeviceCollector

from htss.devices import sample, det, beam, _calculate_estimated_time, ParameterOutsideLimits

import pytest

from unittest.mock import MagicMock, patch

from htss.run_plans_here import RE

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

def test_set_is_called_with_correct_arguments():
    mock_estimated_time.assert_called_with(x_param=15, timeout=20)
    pass

def test_after_using_set_then_previous_positions_are_correct():
    ...

def test_read_gives_correct_values():
    ...

def test_our_mock():
    with patch("htss.devices._calculate_estimated_time") as mock_estimated_time:
        mock_estimated_time.return_value(15)

        mock_estimated_time.assert_called_with()



#test_if_position_not_within_limits_and_exception_raised()
#test_if_position_within_limits_then_no_exception_raised()
#test_given_distance_and_velocity_then_calculated_time_is_correct()