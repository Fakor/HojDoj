import unittest

EPSILON = 4


class HojdojTestCase(unittest.TestCase):

    def assertUpdateEqual(self, u1, u2):
        self.assertEqual(len(u1), len(u2))
        for el1, el2 in zip(u1, u2):
            self.assertEqual(el1[0], el2[0])
            self.assertFloatTupleEqual(el1[1], el2[1])

    def assertFloatTupleEqual(self, t1, t2):
        self.assertEqual(len(t1), len(t2))
        for el1, el2 in zip(t1, t2):
            self.assertAlmostEqual(el1, el2, EPSILON)

    def callback(self, actions):
        return actions