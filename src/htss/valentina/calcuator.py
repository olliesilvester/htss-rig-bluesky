class NegativeValueError(Exeption):
    pass
class OddValueError(Exeption):
    pass
class InappropriateInputError(Exeption):
    pass
num1 = int(input("Input the first number: "))
num2 = int(input("Input the second number: "))

def calculate(numm1, num2):
    total = num1 + num2
    if total < 0:
        raise NegativeValueError(f"Total {total} is less than zero")
    elif  total MOD / 2 = 0:
        raise OddValueError(f"Total {total} is an odd number")
    elif num1 != str or num2 != str:
        raise InappropriateInputError(f"The numbers inputted are not usable")
