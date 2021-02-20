"""Module for math wrapper classes"""
import numbers


class Function:
    """Gives all mathematical funcitons a common interface to react with"""

    def __init__(self, func):
        self.func = func

    def execute(self, element, debug=False):
        """Execute the given function of the element"""
        # Check type
        if not isinstance(element, numbers.Number):
            raise TypeError("The element must be a number")

        result = self.func(element)
        # Report
        if debug:
            print(f"Function: {self.func.__name__}. Input: {element:.2f}. Output: {result:.2f}")

        return result

    def __str__(self):
        return self.func.__name__


class Operator:
    """Gives all mathematical operators a common interface to react with"""

    def __init__(self, operator, strength):
        self.operator = operator
        self.strength = strength

    def execute(self, element1, element2, debug=False):
        """Execute the given function of the element"""
        # Check type
        if not (isinstance(element1, numbers.Number) and isinstance(element2, numbers.Number)):
            raise TypeError("Both elements must be numbers")

        result = self.operator(element1, element2)
        # Report
        if debug:
            print(f"""Operator: {self.operator.__name__}.
            Inputs: {element1:.2f}, {element2:.2f}. 
            Output:{result:.2f}""")

        return result

    def __str__(self):
        return self.operator.__name__
