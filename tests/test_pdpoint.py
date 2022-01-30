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
        self.assertEqual(a.dist(b), 1)

    def test_point_from_string(self):
        self.assertEqual(PDPoint.fromstring("0 5"), PDPoint((0,5)))

    def test_point_index(self):
        a = PDPoint((0,5))
        self.assertEqual(a[0], 0)
        self.assertEqual(a[1], 5)

    def test_point_equals(self):
        a = PDPoint((0,5))
        b = PDPoint((0,6))
        c = PDPoint((0,5))
        self.assertEqual(a, c)
        self.assertNotEqual(a, b)
    
    def test_diagonal_projection(self):
        P = PDPoint((3,8))
        self.assertEqual(P.diagproj(), PDPoint((5.5,5.5)))

    def test_pp_dist(self):
        a = PDPoint((0,7))
        b = PDPoint((2,8))
        c = PDPoint((8,10))
        d = PDPoint((0,2))
        self.assertEqual(a.pp_dist(b), 2)
        self.assertEqual(c.pp_dist(d), 2)
    
    def test_is_diagonal_point(self):
        self.assertTrue(PDPoint((5,5)).isdiagonalpoint())
        self.assertFalse(PDPoint((5,8)).isdiagonalpoint())

if __name__=='__main__':
    unittest.main()