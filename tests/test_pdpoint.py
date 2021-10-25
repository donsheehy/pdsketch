import unittest
from pdsketch import PDPoint

class TestPDPoint(unittest.TestCase):
    def test_valid_point(self):
        self.assertRaises(ValueError, PDPoint, (5,0))
        self.assertRaises(TypeError, PDPoint, (5))
        self.assertRaises(TypeError, PDPoint, (5,0,6))

    def test_point_distance(self):
        a = PDPoint((0,5))
        b = PDPoint((0,6))
        assert a.dist(b) == 1

    def test_point_from_string(self):
        assert PDPoint.fromstring("0 5") == PDPoint((0,5))

    def test_point_index(self):
        a = PDPoint((0,5))
        assert a[0] == 0
        assert a[1] == 5

    def test_point_equals(self):
        a = PDPoint((0,5))
        b = PDPoint((0,6))
        c = PDPoint((0,5))
        assert a == c
        assert a != b

if __name__=='__main__':
    unittest.main()