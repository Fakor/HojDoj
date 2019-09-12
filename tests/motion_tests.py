import unittest

from logic.sketch_logic import SketchLogic
from logic.image_logic import ImageLogic
from DTools.tools import count_jump_range

from constants import *
from functions import *
from hojdoj_testcase import *


class MotionTests(HojdojTestCase):

    def test_set_velocity(self):
        sketch = SketchLogic(IMAGE_TEMPLATES)

        sketch.draw_object(draw_callback, 'SQUARE', (0, 0), (10, 5), index=7)

        updated = sketch.step()
        self.assertListEqual(updated, [])

        index, velocity = sketch.set_velocity(velocity_callback, (1.5, -2), range=6.25)
        self.assertEqual(index, 7)
        self.assertEqual(velocity, (1.5, -2))

        updated = sketch.step()
        self.assertUpdateEqual(updated, [(7, (1.5, -2))])
        self.assertFloatTupleEqual(sketch.object_position(7), (1.5,  -2))
        updated = sketch.step()
        self.assertUpdateEqual(updated, [(7, (3, -4))])
        self.assertFloatTupleEqual(sketch.object_position(7), (3,  -4))

        updated = sketch.step()
        self.assertUpdateEqual(updated, [(7, (3.75, -5))])
        self.assertFloatTupleEqual(sketch.object_position(7), (3.75,  -5))

        updated = sketch.step()
        self.assertListEqual(updated, [])
        self.assertFloatTupleEqual(sketch.object_position(7), (3.75,  -5))

    def test_set_acceleration(self):
        sketch = SketchLogic(IMAGE_TEMPLATES)

        sketch.draw_object(draw_callback, 'SQUARE', (0, 0), (10, 5), index=5)
        index, acceleration = sketch.set_acceleration(acceleration_callback, (-0.2, 0.5), index=5)
        self.assertEqual(index, 5)
        self.assertEqual(acceleration, (-0.2, 0.5))
        self.assertEqual(sketch.object_velocity(5), (0, 0))
        self.assertEqual(sketch.object_position(5), (0, 0))

        updated = sketch.step()
        self.assertUpdateEqual(updated, [(5, (-0.2, 0.5))])
        self.assertFloatTupleEqual(sketch.object_position(5), (-0.2, 0.5))
        self.assertFloatTupleEqual(sketch.object_velocity(5), (-0.2, 0.5))

        updated = sketch.step()
        self.assertUpdateEqual(updated, [(5, (-0.6, 1.5))])
        self.assertFloatTupleEqual(sketch.object_position(5), (-0.6, 1.5))
        self.assertFloatTupleEqual(sketch.object_velocity(5), (-0.4, 1))

    def test_set_motion(self):
        sketch = SketchLogic(IMAGE_TEMPLATES)

        sketch.draw_object(draw_callback, 'SQUARE', (0, 0), (10, 5), index=5)
        sketch.set_motion(index=5, velocity=(2, 4))

        self.assertFloatTupleEqual(sketch.object_position(5), (0, 0))
        self.assertFloatTupleEqual(sketch.object_velocity(5), (2, 4))
        self.assertFloatTupleEqual(sketch.object_acceleration(5), (0, 0))
        self.assertIsNone(sketch.object_range(5))

        sketch.set_motion(index=5, acceleration=(1, -1), range=100)

        self.assertFloatTupleEqual(sketch.object_position(5), (0, 0))
        self.assertFloatTupleEqual(sketch.object_velocity(5), (2, 4))
        self.assertFloatTupleEqual(sketch.object_acceleration(5), (1, -1))
        self.assertEqual(sketch.object_range(5), 100)

    def test_count_jump_range(self):
        rng = count_jump_range((1, 2), (0, -0.9))
        self.assertAlmostEqual(rng, 8.9269, 3)

    def test_gravity(self):
        i1 = ImageLogic(SQUARE, (1, 1), (2, 1))
        self.assertAlmostEqual(i1.mass, 2)
        i2 = ImageLogic(SQUARE, (4, 5), (3, 2), acceleration=(-1,2))
        self.assertAlmostEqual(i2.mass, 6)

        G = 2.5

        i1.apply_gravity(i2, G)
        self.assertFloatTupleEqual(i1.acceleration, (0.36, 0.48))

        i2.apply_gravity(i1, G)
        self.assertFloatTupleEqual(i2.acceleration, (-1.12, 1.84))
