"""Contains calculator class"""

import re
import numbers
import numpy as np
from math_wrappers import Function, Operator
from container import Queue, Stack


class Calc:
    """Calcualtor for evaluation different expressions"""

    def __init__(self):
        self.functions = {
            'EXP': Function(np.exp),
            'LOG': Function(np.log),
            'SIN': Function(np.sin),
            'COS': Function(np.cos),
            'SQRT': Function(np.sqrt)
        }
        self.operators = {
            'PLUS': Operator(np.add, 0),
            'ADD': Operator(np.add, 0),
            'TIMES': Operator(np.multiply, 1),
            'MULTIPLY': Operator(np.multiply, 1),
            'DIVIDE': Operator(np.divide, 1),
            'MINUS': Operator(np.subtract, 0),
            'SUBTRACT': Operator(np.subtract, 0)
        }

        self.output_queue = Queue()

    def calculate_expression(self, text):
        """Takes an expression in human readable form and calculates the answer"""
        text = self.parse_text(text)
        self.shunting_yard(text)
        answer = self.rpn()
        return answer

    def parse_text(self, text):
        """Parses human readable text into something that is ready to be sorted by shunting_yard"""
        text = text.replace(" ", "").upper()
        index = 0
        shunting_yard_ready = Queue()

        while index < len(text):
            text = text[index:]

            # Check for number
            match = re.search("^[-0123456789.]+", text)
            if match is not None:
                shunting_yard_ready.push(float(match.group(0)))
                index = match.end(0)
                continue

            # Check for function
            match = re.search("|".join(["^" + func for func in self.functions.keys()]), text)
            if match is not None:
                shunting_yard_ready.push(self.functions[match.group(0)])
                index = match.end(0)
                continue

            # Check for operator
            match = re.search("|".join(["^" + op for op in self.operators.keys()]), text)
            if match is not None:
                shunting_yard_ready.push(self.operators[match.group(0)])
                index = match.end(0)
                continue

            # Check for paranthases
            match = re.search("^[()]", text)
            if match is not None:
                shunting_yard_ready.push(match.group(0))
                index = match.end(0)
                continue

        return shunting_yard_ready

    def shunting_yard(self, elements: Queue):
        """Does the shunting yard algorithm to produce something that is ready for rpn"""
        operator_stack = Stack()
        while not elements.is_empty():
            element = elements.pop()

            if isinstance(element, numbers.Number):
                self.output_queue.push(element)
            elif isinstance(element, Function) or element == "(":
                operator_stack.push(element)
            elif element == ")":
                while operator_stack.peek() != "(":
                    self.output_queue.push(operator_stack.pop())

                # Pop (
                if operator_stack.peek() == "(":
                    operator_stack.pop()

                if not operator_stack.is_empty() and isinstance(operator_stack.peek(), Function):
                    self.output_queue.push(operator_stack.pop())
            elif isinstance(element, Operator):
                intermediate_storage = Stack()
                while ((not operator_stack.is_empty())
                       and (not operator_stack.peek() == "(")
                       and operator_stack.peek().strength < element.strength):
                    intermediate_storage.push(operator_stack.pop())

                while not intermediate_storage.is_empty():
                    operator_stack.push(intermediate_storage.pop())

                operator_stack.push(element)

        while not operator_stack.is_empty():
            self.output_queue.push(operator_stack.pop())

    def rpn(self):
        """Evaluates self.output_queue in RPN"""
        intermediate_storage = Stack()
        while not self.output_queue.is_empty():
            item = self.output_queue.pop()
            if isinstance(item, numbers.Number):
                intermediate_storage.push(item)
            elif isinstance(item, Function):
                result = item.execute(intermediate_storage.pop())
                intermediate_storage.push(result)
            elif isinstance(item, Operator):
                operand1 = intermediate_storage.pop()
                operand2 = intermediate_storage.pop()
                result = item.execute(operand2, operand1)
                intermediate_storage.push(result)

        return intermediate_storage.pop()
