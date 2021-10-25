import unittest
from pdsketch import Diagram, PDPoint, l_inf

class TestDiagram(unittest.TestCase):
    def test_diagram_super_methods(self):
        D = Diagram([(0,5),(3,8)])
        a = PDPoint((0,5))
        b = PDPoint((3,8))
        p = iter(D)
        assert next(p) == a
        assert next(p) == b

        assert len(D) == 4
    
    def test_diagonal_projection(self):
        D = Diagram()
        assert D.diagproj(PDPoint((3,8))) == PDPoint((5.5,5.5))
    
    def test_pp_dist(self):
        a = PDPoint((0,7))
        b = PDPoint((2,8))
        c = PDPoint((8,10))
        d = PDPoint((0,2))
        D = Diagram()
        assert D.pp_dist(a,b) == 2
        assert D.pp_dist(c,d) == 2
        # print(D.dist(c,d))

    def test_is_diagonal_point(self):
        D = Diagram()
        assert D.isdiagonalpoint(PDPoint((5,5))) == True
        assert D.isdiagonalpoint(PDPoint((5,8))) == False

    def test_dist(self):
        D = Diagram()
        a = PDPoint((5,5))
        b = PDPoint((2,2))
        c = PDPoint((0,2))
        d = PDPoint((2,8))
        assert D.dist(a,b) == 3
        assert D.dist(c,d) == 6
        assert D.dist(a,c) == 1

    def test_compare_dist(self):
        D = Diagram()
        a = PDPoint((5,5))
        b = PDPoint((2,2))
        c = PDPoint((0,2))
        d = PDPoint((2,8))
        
        assert D.comparedist(c, a, b) == False

if __name__=='__main__':
    unittest.main()