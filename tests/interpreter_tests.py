import unittest

from logic.sketch_logic import SketchLogic
from logic.interpreter import Interpreter, interpret_values, arg_split
from constants import *


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

    def test_draw_command(self):
        sketch = SketchLogic(IMAGE_TEMPLATES)
        interpreter = Interpreter(sketch.get_command_table())

        interpreter.perform_command("draw(SQUARE, (5,7), (3,8), index=5)")

        self.assertEqual(sketch.object_position(5), (5,7))
        self.assertEqual(sketch.object_size(5), (3, 8))


if __name__ == '__main__':
    unittest.main()
