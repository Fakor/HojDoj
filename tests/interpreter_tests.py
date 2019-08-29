import unittest

from logic.sketch_logic import SketchLogic
from logic.interpreter import Interpreter, interpret_values, arg_split
from constants import *
from functions import *


class InterpreterTests(unittest.TestCase):
    def test_arg_split(self):
        values = arg_split("SQUARE, 4, 6.7, (5,7), index=5, position=(5,6))")
        expected_values = ['SQUARE', '4', '6.7', '(5,7)', 'index=5', 'position=(5,6)']
        self.assertListEqual(values, expected_values)

    def test_interpret_values(self):
        values = ['SQUARE', '4', '6.7', '(5,7)', 'index=5', 'position=(5,6)']
        args, kwargs = interpret_values(values)

        expected_args = ['SQUARE', 4, 6.7, (5,7)]
        expected_kwargs = {
            'index': 5,
            'position':(5, 6)
        }

        self.assertListEqual(args, expected_args)
        self.assertDictEqual(kwargs, expected_kwargs)


if __name__ == '__main__':
    unittest.main()
