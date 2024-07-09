
class ValueNegative(Exception):
    pass
class ValueOdd(Exception):
    pass
class TotalOdd(Exception):
    pass

def calculator():
    try:
        num1 = input(">")
        num2 = input(">")
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
        print("Idk")
    except ValueOdd:
        print("Haha")
    except TotalOdd:
        print("Something")
    except TypeError:
        print("Type error but i defined it.")


calculator()



