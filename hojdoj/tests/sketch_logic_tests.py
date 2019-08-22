import unittest

from logic.sketch_logic import SketchLogic


class MyTestCase(unittest.TestCase):
    def test_mark_object(self):
        sketch = SketchLogic()
        self.assertEqual(sketch.x, 1)


if __name__ == '__main__':
    unittest.main()
