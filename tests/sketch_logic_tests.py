import unittest

from logic.sketch_logic import SketchLogic
from constants import *
from functions import *


class SketchLogicTests(unittest.TestCase):
    def test_mark_object(self):
        sketch = SketchLogic(IMAGE_TEMPLATES)

        self.assertEqual(sketch.draw_object(draw_callback, 'SQUARE', (0,0), (10, 10)), (0, (0,0)))
        self.assertEqual(sketch.draw_object(draw_callback,'SQUARE', (0, 0), (10, 10)), (1, (0,0)))
        self.assertEqual(sketch.draw_object(draw_callback,'SQUARE', (0, 0), (10, 10), index=10), (10, (0,0)))

        self.assertIsNone(sketch.mark_object(mark_callback, (-15, 0)))
        self.assertIsNone(sketch.mark_object(mark_callback, (0, -15)))
        self.assertIsNone(sketch.mark_object(mark_callback, (15, 15)))

        self.assertEqual(sketch.mark_object(mark_callback, (0, 0)), 10)
        self.assertEqual(sketch.delete_object(delete_callback, 10), 10)
        self.assertEqual(sketch.mark_object(mark_callback, (0, 0)), 1)
        self.assertEqual(sketch.delete_object(delete_callback, 1), 1)
        self.assertEqual(sketch.mark_object(mark_callback, (0, 0)), 0)
        self.assertEqual(sketch.delete_object(delete_callback, 0), 0)
        self.assertIsNone(sketch.mark_object(mark_callback, (0, 0)))

    def test_move_object(self):
        sketch = SketchLogic(IMAGE_TEMPLATES)

        sketch.draw_object(draw_callback, 'SQUARE', (30, 20), (10, 5), index=0)
        self.assertEqual(sketch.object_position(0), (30, 20))
        self.assertEqual(sketch.object_size(0), (10, 5))

        self.assertEqual(sketch.move_object(move_callback, 0, (-5, 15)), (0, (25,35)))
        self.assertEqual(sketch.object_position(0), (25,35))

    def test_move_object_intermediate(self):
        sketch = SketchLogic(IMAGE_TEMPLATES)
        sketch.draw_object(draw_callback, 'SQUARE', (30, 20), (10, 5), index=0)

        index, intermediate_pos = sketch.move_object(move_callback, 0, (10, -15), intermediate=True)
        self.assertEqual(intermediate_pos, (40, 5))
        self.assertEqual(sketch.object_position(0), (30,  20))

    def test_rotate_object(self):
        sketch = SketchLogic(IMAGE_TEMPLATES)

        sketch.draw_object(draw_callback, 'SQUARE', (30, 20), (10, 5), index=0)
        self.assertEqual(sketch.object_rotation(0), 0)

        index, rotation = sketch.rotate_object(rotate_callback, 0, 20)
        self.assertEqual(rotation, 20)
        self.assertEqual(sketch.object_rotation(index), 20)

        index, rotation = sketch.rotate_object(rotate_callback, 0, 20)
        self.assertEqual(rotation, 20)
        self.assertEqual(sketch.object_rotation(index), 40)

    def test_rotate_object_intermediate(self):
        sketch = SketchLogic(IMAGE_TEMPLATES)

        sketch.draw_object(draw_callback, 'SQUARE', (30, 20), (10, 5), index=0)
        self.assertEqual(sketch.object_rotation(0), 0)

        index, rotation = sketch.rotate_object(rotate_callback, 0, 20, intermediate=True)
        self.assertEqual(rotation, 20)
        self.assertEqual(sketch.object_rotation(index), 0)

    def test_resize_object(self):
        sketch = SketchLogic(IMAGE_TEMPLATES)

        sketch.draw_object(draw_callback, 'SQUARE', (30, 20), (10, 5), index=0)
        self.assertEqual(sketch.object_size(0), (10, 5))

        index, size = sketch.resize_object(resize_callback, 0, (-3, 5))
        self.assertEqual(size, (7, 10))
        self.assertEqual(sketch.object_size(index), (7, 10))

        index, size = sketch.resize_object(resize_callback, 0, (-10, 7))
        self.assertEqual(size, (0, 17))
        self.assertEqual(sketch.object_size(index), (0, 17))

    def test_resize_object_intermediate(self):
        sketch = SketchLogic(IMAGE_TEMPLATES)

        sketch.draw_object(draw_callback, 'SQUARE', (30, 20), (10, 5), index=0)
        self.assertEqual(sketch.object_size(0), (10, 5))

        index, size = sketch.resize_object(resize_callback, 0, (-3, 5), intermediate=True)
        self.assertEqual(size, (7, 10))
        self.assertEqual(sketch.object_size(index), (10, 5))

        index, size = sketch.resize_object(resize_callback, 0, (-10, 7))
        self.assertEqual(size, (0, 12))
        self.assertEqual(sketch.object_size(index), (0, 12))


if __name__ == '__main__':
    unittest.main()
