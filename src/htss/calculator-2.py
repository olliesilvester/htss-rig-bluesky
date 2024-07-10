import pytest
from unittest.mock import patch
class ValueNegative(Exception):
    pass
class ValueOdd(Exception):
    pass
class TotalOdd(Exception):
    pass

def calculator():
    try:
        num1 = int(input(">"))
        num2 = int(input(">"))
        if num1 < 0 or num2 < 0:
            raise ValueNegative
        elif num1 % 2 != 0 or num2 % 2 != 0:
            raise ValueOdd
        total = num1 + num2
        if total % 2 != 0:
            raise TotalOdd
        else:
            return num1, num2
    except ValueNegative:
        print("Inputs must be positive.")
    except ValueOdd:
        print("Inputs must be even.")
    except TotalOdd:
        print("Total must be an even number.")
    except ValueError:
        print("Inputs must be integers or floats.")

@patch("builtins.print")
def test_if_inputs_are_negative_custom_exception_raised(mock_print):
    with patch("builtins.input", side_effect = [-2,4]):
        calculator()
    mock_print.assert_called_with("Inputs must be positive.")

@patch("builtins.print")
def test_if_inputs_are_odd_custom_exception_raised(mock_print):
    with patch("builtins.input", side_effect = [3,2]):
        calculator()
    mock_print.assert_called_with("Inputs must be even.")


def test_if_inputs_and_total_valid_return_user_inputs():
    with patch("builtins.input", side_effect = [6,8]):
        calculator()
     

@patch("builtins.print")
def test_if_type_error_handled_appropriately(mock_print):
    with patch("builtins.input", side_effect = ["arrow", True]):
        calculator()
    mock_print.assert_called_with("Inputs must be integers or floats.")


    


# test_if_inputs_are_negative_custom_exception_raised()
# test_if_inputs_are_odd_custom_exception_raised()
# test_if_inputs_and_total_valid_return_user_inputs()
test_if_type_error_handled_appropriately()
