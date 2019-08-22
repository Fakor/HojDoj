import unittest
import os

from logic.sketch_logic import SketchLogic
from logic.image_logic import ImageLogic


SQUARE = '{}/resources/square.png'.format(os.environ['TEST_FOLDER'])


class MyTestCase(unittest.TestCase):
    def test_mark_object(self):
        sketch = SketchLogic()

        sketch.add_object(0, ImageLogic(SQUARE, (0,0), (10,10)))
        sketch.add_object(1, ImageLogic(SQUARE, (0, 0), (10, 10)))
        sketch.add_object(2, ImageLogic(SQUARE, (0, 0), (10, 10)))

        self.assertIsNone(sketch.mark_object(-15, 0))
        self.assertIsNone(sketch.mark_object(0, -15))
        self.assertIsNone(sketch.mark_object(15, 15))

        self.assertEqual(sketch.mark_object(0, 0), 2)
        sketch.delete(2)
        self.assertEqual(sketch.mark_object(0, 0), 1)
        sketch.delete(1)
        self.assertEqual(sketch.mark_object(0, 0), 0)
        sketch.delete(0)
        self.assertIsNone(sketch.mark_object(0, 0))


if __name__ == '__main__':
    unittest.main()
