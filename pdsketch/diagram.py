from typing import DefaultDict
from pdsketch import PDPoint
from metricspaces import MetricSpace
from pdsketch.distance import l_inf

class Diagram(MetricSpace):
    """
    A class to store persistence diagrams.
    This class represents the space of PDs and is designed to run as a quotient of a metric space.
    Main input is a list of points in the persistence plane.
    Allows for multiplicity in input.
    """
    def __init__(self, X=()):
        super().__init__([PDPoint(p) for p in X], dist=self.dist)

    def dist(self, a:PDPoint, b:PDPoint)->float:
        """
        Compute distance between points `a` and `b`.

        If both `a` and `b` are on the diagonal or both are off the diagonal
         then the method returns the l_inf distance between `a` and `b`.
        If one point is on the diagonal and the other is off diagonal then
         the method returns the quotient distance between `a` and `b`.
        """
        if a.isdiagonalpoint() == b.isdiagonalpoint():
            return a.dist(b)
        else:
            return a.pp_dist(b)
    
    def comparedist(self, x:PDPoint, a:PDPoint, b:PDPoint, alpha:float=1)->bool:
        """
        Check if `a` is closer to `x` than `b` .

        Overrides method in MetricSpace.

        Comparison is done on a tuple of the persistence plane distance
         and l_inf distance.
        """
        return ((x.pp_dist(a), x.dist(a)) < 
                (alpha*x.pp_dist(b), alpha*x.dist(b)))

    # def loadfromfile():
    #     pass

    # def savetofile():
    #     pass