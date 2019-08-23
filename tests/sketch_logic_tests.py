import unittest
import os

from logic.sketch_logic import SketchLogic
from logic.image_logic import ImageLogic


SQUARE = '{}/resources/square.png'.format(os.environ['TEST_FOLDER'])


class MyTestCase(unittest.TestCase):
    def test_mark_object(self):
        sketch = SketchLogic()

        self.assertEqual(sketch.add_object(ImageLogic(SQUARE, (0,0), (10,10))), 0)
        self.assertEqual(sketch.add_object(ImageLogic(SQUARE, (0, 0), (10, 10))), 1)
        self.assertEqual(sketch.add_object(ImageLogic(SQUARE, (0, 0), (10, 10)), index=10), 10)

        self.assertIsNone(sketch.mark_object(-15, 0))
        self.assertIsNone(sketch.mark_object(0, -15))
        self.assertIsNone(sketch.mark_object(15, 15))

        self.assertEqual(sketch.mark_object(0, 0), 10)
        sketch.delete_object(10)
        self.assertEqual(sketch.mark_object(0, 0), 1)
        sketch.delete_object(1)
        self.assertEqual(sketch.mark_object(0, 0), 0)
        sketch.delete_object(0)
        self.assertIsNone(sketch.mark_object(0, 0))

    def test_move_object(self):
        sketch = SketchLogic()

        sketch.add_object(ImageLogic(SQUARE, (30,20), (10,10)), 0)
        self.assertEqual(sketch.object_position(0), (30,20))

        sketch.move_object(0, (-5, 15))
        self.assertEqual(sketch.object_position(0), [25,35])


if __name__ == '__main__':
    unittest.main()
