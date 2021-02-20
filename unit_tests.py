"""Module for unit tests of the calculator project"""

import unittest
from math import e
import numpy as np
from container import Stack, Queue
from math_wrappers import Function, Operator
from calc import Calc


class ContainerTest(unittest.TestCase):
    """Test of container and subclasses"""
    test_list = [1, 2, 3, 4, 5]

    def test_stack(self):
        """Test Stack class"""

        stack = Stack()
        for num in self.test_list:
            stack.push(num)

        index_from_end = 1
        while not stack.is_empty():
            num = stack.pop()
            self.assertEqual(num, self.test_list[-index_from_end])
            index_from_end += 1

    def test_queue(self):
        """Test Queue class"""

        queue = Queue()
        for num in self.test_list:
            queue.push(num)

        index = 0
        while not queue.is_empty():
            num = queue.pop()
            self.assertEqual(num, self.test_list[index])
            index += 1


class FunctionTest(unittest.TestCase):
    """Test of the Function class"""

    def test_exp(self):
        """Test that np exp function works"""
        func = Function(np.exp)
        self.assertEqual(round(func.execute(3), 3), round(e ** 3, 3))


class OperatorTest(unittest.TestCase):
    """Test of the Operator class"""

    def test_multiply(self):
        """Test that np multiply function works"""
        operator = Operator(np.multiply, 1)
        self.assertEqual(operator.execute(7, 8), 7 * 8)


class Caclulatortest(unittest.TestCase):
    """Test of the Calculator class"""

    def test_basic(self):
        """Test that the intializer is correct"""
        calc = Calc()
        self.assertEqual(calc.functions['EXP']
                         .execute(calc.operators['ADD']
                                  .execute(1, calc.operators['MULTIPLY'].
                                           execute(2, 3))), 1096.6331584284585)

    def test_rpn(self):
        """Test that rpn works correctly"""
        calc = Calc()
        calc.output_queue = Queue(
            [1, 2, 3, Operator(np.multiply, 1), Operator(np.add, 0), Function(np.exp)]
        )
        self.assertEqual(round(calc.rpn(), 2), 1096.63)

    def test_shunting_yard(self):
        """Test that shunting yard works correctly"""
        calc = Calc()
        elements = Queue(
            [Function(np.exp), '(', 1, Operator(np.add, 0), 2, Operator(np.multiply, 1), 3, ")"]
        )
        calc.shunting_yard(elements)
        expected_output = Queue(
            [1, 2, 3, Operator(np.multiply, 1), Operator(np.add, 0), Function(np.exp)]
        )
        self.assertEqual(str(expected_output), str(calc.output_queue))

    def test_parse_text(self):
        """Test that text parser works correctly"""
        calc = Calc()
        output = calc.parse_text("2 multiply 3 add 1")
        expected_output = Queue([2.0, Operator(np.multiply, 1), 3.0, Operator(np.add, 0), 1.0])
        self.assertEqual(str(expected_output), str(output))

    def test_full(self):
        """Test the full calculator"""
        calc = Calc()

        self.assertEqual(round(
            calc.calculate_expression("EXP (1 add 2 multiply 3)"), 2),
            1096.63)
        self.assertEqual(
            calc.calculate_expression(
                "((15 DIVIDE (7 SUBTRACT (1 ADD 1))) MULTIPLY 3) SUBTRACT (2 ADD (1 ADD 1))"
            ),
            5.0)
        print(calc.calculate_expression("SIN(3.14 DIVIDE 2) ADD 1"))

if __name__ == '__main__':
    unittest.main()
