import unittest
from pdsketch import Diagram, SketchSequence, PDPoint

class TestSketchSequence(unittest.TestCase):
    def test_dunder_mathods(self):
        D = Diagram([(12,15), (12,16)])
        S = SketchSequence(D)
        sketch_iter = iter(S)
        sketch = next(sketch_iter)
        self.assertEqual(sketch['point'], PDPoint([0,0]))
        self.assertEqual(sketch['parent_index'], None)
        S_2 = SketchSequence(D)
        self.assertEqual(hash(S), hash(S_2))

    def test_sketch_zeroth(self):
        D = Diagram([(12,15), (12,16)])
        S = SketchSequence(D)
        self.assertEqual(S[0], Diagram([(0,0)],[2]))

    def test_sketch_point_moved_from_diagonal(self):
        D = Diagram([(12,15), (12,16)])
        S = SketchSequence(D)
        a = PDPoint([12,16])
        diagonal = PDPoint([0,0])
        self.assertEqual(S._sketches[1]['transport_plan'][a], 2)
        self.assertEqual(S._sketches[1]['transport_plan'][diagonal], -2)
        self.assertEqual(S[1], Diagram([(12,16)], [2]))
    
    def test_sketch_final(self):
        D = Diagram([(12,15), (12,16)])
        S = SketchSequence(D)
        a = PDPoint([12,16])
        b = PDPoint([12,15])
        self.assertEqual(S._sketches[2]['transport_plan'][a], -1)
        self.assertEqual(S._sketches[2]['transport_plan'][b], 1)
        self.assertEqual(S[2], D)

    def test_first_point_is_farthest(self):
        D = Diagram([(1,19), (22,38), (2,3)])
        S = SketchSequence(D)
        a = PDPoint([1,19])
        b = PDPoint([22,38])
        c = PDPoint([2,3])
        self.assertEqual(S._sketches[1]['point'], a)
        self.assertEqual(S._sketches[2]['point'], b)
        self.assertEqual(S._sketches[3]['point'], c)

    def test_sketch_bottleneck(self):
        D = Diagram([(1,19), (22,38), (2,3)])
        S = SketchSequence(D)
        a = PDPoint([1,19])
        b = PDPoint([22,38])
        c = PDPoint([2,3])
        self.assertEqual(S.sketch_bottleneck(0), 9)
        self.assertEqual(S.sketch_bottleneck(1), 8)
        self.assertEqual(S.sketch_bottleneck(2), 0.5)
        self.assertEqual(S.sketch_bottleneck(3), None)

    def test_sketch_file(self):
        D = Diagram([(1,19), (22,38), (2,3)])
        S = SketchSequence(D)
        S.savetofile("test_sketch.txt")
        sketches = S._sketches
        S.loadfromfile("test_sketch.txt")
        self.assertEqual(sketches, S._sketches)

if __name__ == '__main__':
    unittest.main()