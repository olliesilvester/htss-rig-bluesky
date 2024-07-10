import pytest
from unittest.mock import patch

class NegativeValueError(Exception):
    pass
class OddValueError(Exception):
    pass

def calculate():
    try:
        num1 = int(input("Input the first number: "))
        num2 = int(input("Input the second number: "))
        total = num1 + num2
        if total < 0:
            raise NegativeValueError(f"Total {total} is less than zero")
        elif  total % 2 == 0:
            raise OddValueError(f"Total {total} is an odd number")
    finally:
        print(f"Yor total is {total}")
    
def test_calculate_raises_error_on_a_negative_input():
    with pytest.raises(NegativeValueError):
        with patch('builtins.input', side_effect = [-4,2]):
            calculate()

def test_calculate_raises_error_on_odd_value():
    with pytest.raises(OddValueError):
        with patch('builtins.input', side_effect = [5,2]):
            calculate()



test_calculate_raises_error_on_a_negative_input()
test_calculate_raises_error_on_odd_value()