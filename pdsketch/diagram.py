from typing import DefaultDict
from pdsketch import PDPoint
from metricspaces import MetricSpace
from pdsketch.distance import l_inf

class Diagram(MetricSpace):
    """
    A class to store persistence diagrams.
    This class represents the space of PDs and is designed to run as a
    quotient of a metric space.
    Main input is a list of points in the persistence plane.
    Allows for multiplicity in input.
    """
    def __init__(self, X=[]):

        points = [PDPoint(p) for p in X]
        # Append list of projections
        points += [self.diagproj(p) for p in points]

        super().__init__(points, dist=self.dist)
        self.comparedist = self.comparedist

    def diagproj(self, a:PDPoint)->PDPoint:
        """
        Compute the projection of a point `a` on the diagonal.
        """
        return PDPoint([(a[0]+a[1])/2, (a[0]+a[1])/2])

    def pp_dist(self, a:PDPoint, b:PDPoint)->float:
        """
        Compute quotient distance in the persistence plane.
        The diagonal is treated as a single point.
        """
        return min(l_inf(a, b), l_inf(a, self.diagproj(a))+l_inf(b, self.diagproj(b)))
    
    def isdiagonalpoint(self, a:PDPoint)->bool:
        """
        Check if `a` is a diagonal point.
        """
        return a[0]==a[1]

    def dist(self, a:PDPoint, b:PDPoint)->float:
        """
        Compute distance between points `a` and `b`.

        If both `a` and `b` are on the diagonal or both are off the diagonal
         then the method returns the l_inf distance between `a` and `b`.
        If one point is on the diagonal and the other is off diagonal then
         the method returns the quotient distance between `a` and `b`.
        """
        if self.isdiagonalpoint(a) == self.isdiagonalpoint(b):
            return l_inf(a,b)
        else:
            return self.pp_dist(a, b)
    
    def comparedist(self, x:PDPoint, a:PDPoint, b:PDPoint, alpha:float=1)->bool:
        """
        Check if `a` is closer to `x` than `b` .

        Overrides method in MetricSpace.

        Comparison is done on a tuple of the persistence plane distance
         and l_inf distance.
        """
        return ((self.pp_dist(x, a), l_inf(x, a)) < 
                (alpha*self.pp_dist(x, b), alpha*l_inf(x, b)))

    def loadfromfile():
        pass

    def savetofile():
        pass