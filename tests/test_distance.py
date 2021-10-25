import unittest
from pdsketch import PDPoint, l_inf, l_p

class TestDistance(unittest.TestCase):
    def test_l_inf(self):
        a = PDPoint((0,5))
        b = PDPoint((0,6))
        c = PDPoint((5,5))
        assert l_inf(a,b) == 1
        assert l_inf(a,c) == 5

    def test_l_p(self):
        a = PDPoint((0,0))
        b = PDPoint((3,4))
        c = PDPoint((5,5))
        assert l_p(a, b, 2) == 5
        assert l_p(b, c, 1) == 3

if __name__=='__main__':
    unittest.main()