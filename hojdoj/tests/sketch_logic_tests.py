from logic.sketch_logic import SketchLogic
from DTools.fillers import *

from tests.resources.helper.constants import *
from tests.resources.helper.hojdoj_testcase import *


class SketchLogicTests(HojdojTestCase):
    def test_mark_object(self):
        sketch = SketchLogic(CONFIG, self.callback)

        self.assertEqual(sketch.draw_object('SQUARE', (0,0), (10, 10)), [('draw', {'index': 0})])
        self.assertEqual(sketch.draw_object('SQUARE', (0, 0), (10, 10)), [('draw', {'index': 1})])
        self.assertEqual(sketch.draw_object('SQUARE', (0, 0), (10, 10), index=10), [('draw', {'index': 10})])

        self.assertEqual(sketch.mark_object((-15, 0)), [])
        self.assertEqual(sketch.mark_object((0, -15)), [])
        self.assertEqual(sketch.mark_object((15, 15)), [])

        self.assertEqual(sketch.mark_object((0, 0)), [('mark', {'index': 10})])
        self.assertEqual(sketch.delete_object(), [('delete', {'index': 10})])
        self.assertEqual(sketch.mark_object((0, 0)), [('mark', {'index': 1})])
        self.assertEqual(sketch.delete_object(index=1), [('delete', {'index': 1})])
        self.assertEqual(sketch.mark_object((0, 0)), [('mark', {'index': 0})])
        self.assertEqual(sketch.delete_object(), [('delete', {'index': 0})])
        self.assertEqual(sketch.mark_object((0, 0)), [])

    def test_move_object(self):
        sketch = SketchLogic(CONFIG, self.callback)

        sketch.draw_object('SQUARE', (30, 20), (10, 5), index=0)
        self.assertEqual(sketch.object_position(0), (30, 20))
        self.assertEqual(sketch.object_size(0), (10, 5))

        self.assertEqual(sketch.move_object((-5, 15)), [('move', {'index': 0, 'position': (25,35)})])
        self.assertEqual(sketch.object_position(0), (25,35))

    def test_move_object_intermediate(self):
        sketch = SketchLogic(CONFIG, self.callback)
        sketch.draw_object('SQUARE', (30, 20), (10, 5), index=0)

        actions = sketch.move_object((10, -15),  index=0, intermediate=True)
        self.assertEqual(actions[0][1]['index'], 0)
        self.assertEqual(actions[0][1]['position'], (40, 5))
        self.assertEqual(sketch.object_position(0), (30,  20))

    def test_rotate_object(self):
        sketch = SketchLogic(CONFIG, self.callback)

        sketch.draw_object('SQUARE', (30, 20), (10, 5), index=0)
        self.assertEqual(sketch.object_rotation(0), 0)

        actions = sketch.rotate_object(20)
        self.assertEqual(actions[0][1]['index'], 0)
        self.assertEqual(actions[0][1]['rotation'], 20)
        self.assertEqual(sketch.object_rotation(0), 20)

        actions = sketch.rotate_object(20, index=0)
        self.assertEqual(actions[0][1]['rotation'], 20)
        self.assertEqual(sketch.object_rotation(0), 40)

    def test_rotate_object_intermediate(self):
        sketch = SketchLogic(CONFIG, self.callback)

        sketch.draw_object('SQUARE', (30, 20), (10, 5), index=0)
        self.assertEqual(sketch.object_rotation(0), 0)

        actions = sketch.rotate_object(20, intermediate=True)
        self.assertEqual(actions[0][1]['index'], 0)
        self.assertEqual(actions[0][1]['rotation'], 20)
        self.assertEqual(sketch.object_rotation(0), 0)

    def test_resize_object(self):
        sketch = SketchLogic(CONFIG, self.callback)

        sketch.draw_object('SQUARE', (30, 20), (10, 5), index=0)
        self.assertEqual(sketch.object_size(0), (10, 5))

        actions = sketch.resize_object((-3, 5))
        self.assertEqual(actions[0][1]['index'], 0)
        self.assertEqual(actions[0][1]['size'], (7,10))
        self.assertEqual(sketch.object_size(0), (7, 10))

        actions = sketch.resize_object((-10, 7), index=0)
        self.assertEqual(actions[0][1]['index'], 0)
        self.assertEqual(actions[0][1]['size'], (0,17))
        self.assertEqual(sketch.object_size(0), (0, 17))

    def test_resize_object_intermediate(self):
        sketch = SketchLogic(CONFIG, self.callback)

        sketch.draw_object('SQUARE', (30, 20), (10, 5), index=0)
        self.assertEqual(sketch.object_size(0), (10, 5))

        actions = sketch.resize_object((-3, 5), intermediate=True)
        self.assertEqual(actions[0][1]['index'], 0)
        self.assertEqual(actions[0][1]['size'], (7,10))
        self.assertEqual(sketch.object_size(0), (10, 5))

        actions = sketch.resize_object((-10, 7))
        self.assertEqual(actions[0][1]['index'], 0)
        self.assertEqual(actions[0][1]['size'], (0,12))

        self.assertEqual(sketch.object_size(0), (0, 12))

    def test_get_color_filler(self):
        sketch = SketchLogic(CONFIG, self.callback)
        filler = sketch.get_filler([100, 150, 200])

        self.assertTrue(isinstance(filler, ColorFiller))
        self.assertEqual(filler.color, [100, 150, 200])

    def test_clear(self):
        sketch = SketchLogic(CONFIG, self.callback)

        sketch.draw_object('SQUARE', (0,0), (10, 10))
        sketch.draw_object('SQUARE', (0, 0), (10, 10))
        sketch.draw_object('SQUARE', (0, 0), (10, 10), index=10)

        self.assertEqual(len(sketch.objects), 3)
        self.assertEqual(sketch.marked_object_index, 10)
        self.assertEqual(sketch.object_index, 1)
        self.assertSetEqual(sketch.used_object_indexes, {0, 1, 10})

        actions = sketch.clear()
        self.assertEqual(actions[0][0], 'clear')

        self.assertEqual(len(sketch.objects), 0)
        self.assertEqual(sketch.marked_object_index, None)
        self.assertEqual(sketch.object_index, 0)
        self.assertSetEqual(sketch.used_object_indexes, set())

if __name__ == '__main__':
    unittest.main()
