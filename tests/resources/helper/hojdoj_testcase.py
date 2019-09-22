import unittest

EPSILON = 4


class HojdojTestCase(unittest.TestCase):

    def assertActionEqual(self, u1, u2):
        self.assertEqual(len(u1), len(u2))
        for el1, el2 in zip(u1, u2):
            self.assertEqual(el1[0], el2[0])
            self.assertEqual(len(el1), len(el2))
            for attribute, value in el1[1].items():
                if isinstance(value, tuple):
                    self.assertFloatTupleEqual(value, el2[1][attribute])
                else:
                    self.assertEqual(value, el2[1][attribute])

    def assertFloatTupleEqual(self, t1, t2):
        self.assertEqual(len(t1), len(t2))
        for el1, el2 in zip(t1, t2):
            self.assertAlmostEqual(el1, el2, EPSILON)

    def callback(self, actions):
        return actions