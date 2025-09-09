import unittest
from pdsketch import Diagram, SketchSequence, PDPoint

class TestSketchSequence(unittest.TestCase):
    def test_dunder_methods(self):
        D = Diagram([(12,15), (12,16)])
        S = SketchSequence(D)
        sketch_iter = iter(S)
        sketch = next(sketch_iter)
        self.assertEqual(sketch.point, PDPoint([13.5,13.5]))
        self.assertEqual(sketch.parent, None)

    def test_sketch_zeroth(self):
        D = Diagram([(12,15), (12,16)])
        S = SketchSequence(D)
        self.assertEqual(S[0], Diagram([(0,0)],[2]))

    def test_sketch_point_moved_from_diagonal(self):
        D = Diagram([(12,15), (12,16)])
        S = SketchSequence(D)
        a = PDPoint([12,16])
        diagonal = PDPoint([13.5,13.5])
        self.assertEqual(S._sketches[1].update_plan[a], 2)
        self.assertEqual(S._sketches[1].update_plan[diagonal], -2)
        self.assertEqual(S[1], Diagram([(12,16)], [2]))

    def test_sketch_final(self):
        a = PDPoint([12,16])
        b = PDPoint([12,15])
        D = Diagram([a,b])
        S = SketchSequence(D)
        self.assertEqual(S._sketches[2].update_plan[a], -1)
        self.assertEqual(S._sketches[2].update_plan[b], 1)
        self.assertEqual(S[2], D)

    def test_first_point_is_farthest(self):
        D = Diagram([(1,19), (22,38), (2,3)])
        S = SketchSequence(D)
        a = PDPoint([1,19])
        b = PDPoint([22,38])
        c = PDPoint([2,3])
        self.assertEqual(S._sketches[1].point, a)
        self.assertEqual(S._sketches[2].point, b)
        self.assertEqual(S._sketches[3].point, c)

    def test_sketch_bottleneck(self):
        D = Diagram([(1,19), (22,38), (2,3)])
        S = SketchSequence(D)
        a = PDPoint([1,19])
        b = PDPoint([22,38])
        c = PDPoint([2,3])
        self.assertEqual(S.sketch_bottleneck(0), 9)
        self.assertEqual(S.sketch_bottleneck(1), 8)
        self.assertEqual(S.sketch_bottleneck(2), 0.5)
        self.assertEqual(S.sketch_bottleneck(3), 0)

    def test_sketch_file(self):
        D = Diagram([(1,19), (22,38), (2,3)])
        S = SketchSequence(D)
        S.save_to_file("test_sketch.txt")
        X = SketchSequence.load_from_file("test_sketch.txt")
        self.assertEqual(S._sketches, X._sketches)


if __name__ == '__main__':
    unittest.main()
