import unittest
from pdsketch import Diagram, PDPoint

class TestDiagram(unittest.TestCase):
    def test_diagram_dunder_methods(self):
        D = Diagram([(0,5),(3,8), [5,5]])
        a = PDPoint((0,5))
        b = PDPoint((3,8))
        diagonal = PDPoint([0,0])
        p = iter(D)
        point_set = set()
        point_set.add(next(p))
        point_set.add(next(p))
        point_set.add(next(p))
        self.assertEqual(point_set, {a, b, diagonal})
        self.assertEqual(len(D), 2)

    def test_diagram_basic(self):
        D = Diagram([(0,5),(3,8)])
        a = PDPoint([0,5])
        b = PDPoint([3,8])
        self.assertRaises(ValueError, Diagram, [(2,5), (5,7)], [1])
        self.assertTrue(a in D)
        self.assertTrue(b in D)
        self.assertEqual(D.mass[a], 1)
        self.assertEqual(D.mass[b], 1)

    def test_diagram_mult(self):
        D = Diagram([(0,5)], [5])
        a = PDPoint([0,5])
        self.assertTrue(a in D)
        self.assertEqual(D.mass[a], 5)

    def test_diagram_add(self):
        D = Diagram()
        a = PDPoint([0,5])
        b = PDPoint([3,8])
        D.add(a)
        D.add(b, 7)
        self.assertTrue(a in D)
        self.assertTrue(b in D)
        self.assertEqual(D.mass[a], 1)
        self.assertEqual(D.mass[b], 7)

    def test_diagram_add_diagonal(self):
        D = Diagram()
        a = PDPoint([5,5])
        b = PDPoint([8,8])
        diagonal = PDPoint([0,0])
        D.add(a, 4)
        D.add(b)
        self.assertTrue(a not in D)
        self.assertTrue(b not in D)
        self.assertTrue(diagonal in D)
        self.assertEqual(D.mass[diagonal], 5)

    def test_diagram_add_neg_mult(self):
        D = Diagram()
        a = PDPoint([0,5])
        D.add(a, 4)
        self.assertTrue(a in D)
        self.assertEqual(D.mass[a], 4)
        D.add(a, -4)
        self.assertTrue(a not in D)

    def test_diagram_remove(self):
        D = Diagram()
        a = PDPoint([0,5])
        self.assertRaises(KeyError, D.remove, a)
        self.assertTrue(a not in D)
        D.add(a)
        self.assertTrue(a in D)
        D.remove(a)
        self.assertTrue(a not in D)

    def test_diagram_clear(self):
        D = Diagram()
        a = PDPoint([0,5])
        b = PDPoint([3,8])
        D.add(a)
        D.add(b, 7)
        self.assertEqual(len(D), 2)
        self.assertNotEqual(len(D.mass), 0)
        D.clear()
        self.assertEqual(len(D), 0)
        self.assertEqual(len(D.mass), 0)

    def test_diagram_get_lists(self):
        a = PDPoint([0,5])
        b = PDPoint([3,8])
        D = Diagram([(0,5),(3,8)], [2,3])
        point, mass = D.get_point_mass_lists()
        self.assertEqual(point, list(dict({a:1,b:1})))
        self.assertEqual(mass, [D.mass[point[0]], D.mass[point[1]]])

    def test_diagram_points(self):
        a = PDPoint([0,5])
        b = PDPoint([3,8])
        D = Diagram([(0,5),(3,8)], [2,3])
        points = D.points()
        self.assertEqual(points, list(dict({a:1,b:1})))

    def test_diagram_file(self):
        D = Diagram([(0,5),(3,8)], [2,3])
        D.save_to_file("test_diagram.txt")
        p, m = D.get_point_mass_lists()
        D_1 = Diagram(p, m)
        Diagram.load_from_file("test_diagram.txt")
        self.assertEqual(D_1, D)

if __name__=='__main__':
    unittest.main()
