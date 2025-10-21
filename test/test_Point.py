from unittest import TestCase
from elliptic_curves.Point import Point

class PointTest(TestCase):

    def test_ne(self):
        a = Point(x=3, y=-7, a=5, b=7)
        b = Point(x=18, y=77, a=5, b=7)
        self.assertTrue(a != b)
        self.assertFalse(a != a)

    def test_eq(self):
        a = Point(x=3, y=-7, a=5, b=7)
        b = Point(x=3, y=-7, a=5, b=7)
        self.assertEqual(a, b)

    def test_add0(self):
        a = Point(x=None, y=None, a=5, b=7)  # point at infinity
        b = Point(x=2, y=5, a=5, b=7)
        c = Point(x=2, y=-5, a=5, b=7)
        self.assertEqual(a + b, b)
        self.assertEqual(b + a, b)
        self.assertEqual(b + c, a)

    def test_add1(self):
        a = Point(x=3, y=7, a=5, b=7)
        b = Point(x=-1, y=-1, a=5, b=7)
        self.assertEqual(a + b, Point(x=2, y=-5, a=5, b=7))

    def test_add2(self):
        a = Point(x=-1, y=-1, a=5, b=7)
        self.assertEqual(a + a, Point(x=18, y=77, a=5, b=7))

    def test_add_different_curves(self):
        a = Point(x=2, y=5, a=5, b=7)
        b = Point(x=None, y=None, a=0, b=7)
        with self.assertRaises(TypeError):
            _ = a + b

    def test_point_not_on_curve(self):
        with self.assertRaises(ValueError):
            Point(x=3, y=7, a=0, b=0)  # not satisfying y^2 = x^3 + ax + b

    def test_double_with_y_zero(self):
        a = Point(x=0, y=0, a=0, b=0)  # (0,0) on curve y^2 = x^3
        self.assertEqual(a + a, Point(x=None, y=None, a=0, b=0))
