from logic.sketch_logic import SketchLogic
from logic.image_logic import ImageLogic
from DTools.tools import count_jump_range

from tests.resources.helper.constants import *
from tests.resources.helper.hojdoj_testcase import *


class MotionTests(HojdojTestCase):

    def test_set_velocity(self):
        sketch = SketchLogic(CONFIG, self.callback)

        sketch.draw_object('SQUARE', (0, 0), (10, 5), index=7)

        updated = sketch.step()
        self.assertListEqual(updated, [])

        actions = sketch.set_motion(velocity=(1.5, -2), range=6.25)
        self.assertEqual(actions, [('motion', {'index': 7})])

        updated = sketch.step()
        self.assertActionEqual(updated, [('move', {'index': 7, 'position': (1.5, -2.0)})])
        self.assertFloatTupleEqual(sketch.object_position(7), (1.5,  -2))
        updated = sketch.step()
        self.assertActionEqual(updated, [('move', {'index': 7, 'position': (3, -4)})])
        self.assertFloatTupleEqual(sketch.object_position(7), (3,  -4))

        updated = sketch.step()
        self.assertActionEqual(updated, [('move', {'index': 7, 'position': (3.75, -5)})])
        self.assertFloatTupleEqual(sketch.object_position(7), (3.75,  -5))

        updated = sketch.step()
        self.assertListEqual(updated, [])
        self.assertFloatTupleEqual(sketch.object_position(7), (3.75,  -5))

    def test_set_acceleration(self):
        sketch = SketchLogic(CONFIG, self.callback)

        sketch.draw_object('SQUARE', (0, 0), (10, 5), index=5)
        actions = sketch.set_motion(acceleration=(-0.2, 0.5), index=5)
        self.assertEqual(actions, [('motion', {'index': 5})])

        self.assertEqual(sketch.object_acceleration(5), (-0.2, 0.5))
        self.assertEqual(sketch.object_velocity(5), (0, 0))
        self.assertEqual(sketch.object_position(5), (0, 0))

        updated = sketch.step()
        self.assertActionEqual(updated, [('move', {'index': 5, 'position': (-0.2, 0.5)})])
        self.assertFloatTupleEqual(sketch.object_position(5), (-0.2, 0.5))
        self.assertFloatTupleEqual(sketch.object_velocity(5), (-0.2, 0.5))

        updated = sketch.step()
        self.assertActionEqual(updated, [('move', {'index': 5, 'position': (-0.6, 1.5)})])
        self.assertFloatTupleEqual(sketch.object_position(5), (-0.6, 1.5))
        self.assertFloatTupleEqual(sketch.object_velocity(5), (-0.4, 1))

    def test_set_motion(self):
        sketch = SketchLogic(CONFIG, self.callback)

        sketch.draw_object('SQUARE', (0, 0), (10, 5), index=5)
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
        rng = count_jump_range((0,1), (0, -0.5))
        self.assertAlmostEqual(rng, 1)

    def test_image_apply_gravity(self):
        ImageLogic.GRAVITY_MIN_RANGE = 0
        i1 = ImageLogic(SQUARE, (1, 1), (2, 1))
        self.assertAlmostEqual(i1.mass, 2)
        i2 = ImageLogic(SQUARE, (4, 5), (3, 2), acceleration=(-1,2))
        self.assertAlmostEqual(i2.mass, 6)

        g = 2.5
        i1.apply_gravity(i2, g)
        self.assertFloatTupleEqual(i1.acceleration, (0.36, 0.48))

        i2.apply_gravity(i1, g)
        self.assertFloatTupleEqual(i2.acceleration, (-1.12, 1.84))

    def test_apply_gravity_all(self):
        ImageLogic.GRAVITY_MIN_RANGE = 0
        sketch = SketchLogic(CONFIG, self.callback)

        sketch.draw_object('SQUARE', (0, 0), (1, 1), index=0, mass=5, acceleration=(5, -5))
        sketch.draw_object('SQUARE', (2, 0), (1, 1), index=1, mass=1)
        sketch.draw_object('SQUARE', (0, 1), (1, 1), index=2, mass=10, acceleration=(1, -2))

        sketch.apply_gravity_all()

        self.assertFloatTupleEqual(sketch.object_acceleration(0), (6.25, 45))
        self.assertFloatTupleEqual(sketch.object_acceleration(1), (-15.19427, 4.4721))
        self.assertFloatTupleEqual(sketch.object_acceleration(2), (1.89442, -27.44721))

        sketch.apply_gravity_all()

        self.assertFloatTupleEqual(sketch.object_acceleration(0), (6.25, 45))
        self.assertFloatTupleEqual(sketch.object_acceleration(1), (-15.19427, 4.4721))
        self.assertFloatTupleEqual(sketch.object_acceleration(2), (1.89442, -27.44721))