from typing import DefaultDict
from pdsketch import PDPoint
from metricspaces import MetricSpace

class Diagram2(MetricSpace):
    """
    A class to store persistence diagrams. Main input is a set of points in the persistence plane.
    Designed to deal with multiplicity in input.
    """
    def __init__(self, X=()):

        points = [PDPoint(p) for p in X]
        # Append list of projections
        points += [self.diagproj(p) for p in points]

        super().__init__(points, dist=self.dist)
        self.comparedist = self.comparedist

    def __iter__(self):
        return iter(self.points)

    def __len__(self):
        return len(self.points)

    def diagproj(self, a):
        return PDPoint([(a[0]+a[1])/2, (a[0]+a[1])/2])

    def l_inf(self, a, b):
        return max(abs(x-y) for x,y in zip(a, b))
    
    def pp_dist(self, a, b):
        return min(self.l_inf(a, b), self.l_inf(a, self.diagproj(a))+self.l_inf(b, self.diagproj(b)))
    
    def isdiagonalpoint(self, a):
        return a[0]==a[1]

    def dist(self, a, b):
        if self.isdiagonalpoint(a) and self.isdiagonalpoint(b):
            return self.l_inf(a, b)
        elif not(self.isdiagonalpoint(a) or self.isdiagonalpoint(b)):
            return self.l_inf(a, b)
        else:
            return self.pp_dist(a, b)
    
    def comparedist(self, x, a, b, alpha=1):
        return ((self.pp_dist(x, a), self.l_inf(x, a)) < 
                (alpha*self.pp_dist(x, b), alpha*self.l_inf(x, b)))

    def loadfromfile():
        pass

    def savetofile():
        pass