import unittest
from pdsketch import Diagram, Sketch, PDPoint

class TestSketch(unittest.TestCase):
    def test_sketch_zeroth(self):
        D = Diagram([(12,15), (13,16)])
        S = Sketch(D)
        assert S[0][PDPoint([0,0])] == 2

    def test_sketch_point_moved_from_diagonal(self):
        D = Diagram([(12,15), (13,16)])
        S = Sketch(D)
        assert S[1][PDPoint([13,16])] == 2
        assert S[1][PDPoint([0,0])] == 0
    
    def test_sketch_final(self):
        D = Diagram([(12,15), (13,16)])
        S = Sketch(D)
        assert S[2][PDPoint([13,16])] == 1
        assert S[2][PDPoint([12,15])] == 1

"""
Example:
D = Diagram([(12,15), (13,16)]) results in the following sketch, S
S[0]= (14.5 14.5, None, defaultdict(<class 'int'>, {0.0 0.0: 2}))
S[1]= (13.0 16.0, 0, defaultdict(<class 'int'>, {13.0 16.0: 2, 0.0 0.0: -2}))
S[2]= (12.0 15.0, 1, defaultdict(<class 'int'>, {0.0 0.0: 0, 13.0 16.0: -1, 12.0 15.0: 1}))
"""

if __name__ == '__main__':
    unittest.main()