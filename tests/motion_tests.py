import unittest

from logic.sketch_logic import SketchLogic

from constants import *
from functions import *


class MotionTests(unittest.TestCase):

    def test_set_motion_speed(self):
        sketch = SketchLogic(IMAGE_TEMPLATES)

        sketch.draw_object(draw_callback, 'SQUARE', (0, 0), (10, 5), index=7)

        updated = sketch.step()
        self.assertListEqual(updated, [])

        index, velocity = sketch.set_velocity_to_object(velocity_callback, (1.5, -2))
        self.assertEqual(index, 7)
        self.assertEqual(velocity, (1.5, -2))

        updated = sketch.step()
        self.assertListEqual(updated, [7])
        self.assertEqual(sketch.object_position(7), (1.5,  -2))
        updated = sketch.step()
        self.assertListEqual(updated, [7])
        self.assertEqual(sketch.object_position(7), (3,  -4))
