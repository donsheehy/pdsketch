from typing import DefaultDict
from pdsketch import QuotientSpace, PDPoint
from metricspaces import MetricSpace

class Diagram(QuotientSpace):
    """
    A class to store persistence diagrams. Main input is a set of points in the persistence plane.
    Designed to deal with multiplicity in input.
    """
    def __init__(self, X=()):

        # Remove any duplicate points that were input. But this multiplicity must be stored somewhere.
        # self.multiplicity stores the number of extra copies (>1) of each point
        # When a sketch transfers a point, this is the mass that gets moved.

        # LATER TRANSFERRED THE MULTIPLICITY COMPUTATION TO NEIGHBORGRAPH.PY. NEED TO REVIEW THIS
        # self.multiplicity = DefaultDict(int)
        # pointset = {}
        # for x in X:
        #     p = Point(x)
        #     if p in pointset:
        #         self.multiplicity[p] += 1
        #     else:
        #         pointset.add(p)
        # # self.points = list(pointset)

        # # Store the number of unique points input
        # self.numpoints = len(pointset)

        points = [PDPoint(p) for p in X]
        # Append list of projections
        points += [self.diagproj(p) for p in points]

        # for p in self.points:
        #     Y.append(self.diagproj(p))
        
        # for p in Y:
        #     if p in X:
        #         self.multiplicity[p] += 1
        #     else:
        #         pointset.add(p)

        # self.points = list(pointset)

        space = MetricSpace(points, dist=self.l_inf)

        super().__init__(space, space[len(X):])

    # def add(self, point, M):
    #     M.append(point)

    def __iter__(self):
        return iter(self.points)

    def __len__(self):
        return len(self.points)

    def diagproj(self, a):
        return PDPoint([(a[0]+a[1])/2, (a[0]+a[1])/2])

    def l_inf(self, a, b):
        return max(abs(x-y) for x,y in zip(a, b))
        
    def loadfromfile():
        pass

    def savetofile():
        pass