from collections import defaultdict
from pdsketch import PDPoint

class Diagram():
    """
    A class to store persistence diagrams.
    Main input is a set of points in the persistence plane with optional multiplicity.
    This implementation is a multiset.
    """

    def __init__(self, points=(), mass:list() = None):
        """
        Parameters
        ----------
        points: list
            The points in the the persistence diagram
        mass: list
            The corresponding multiplicity of points
        """
        if mass == None:
            mass = [1]*len(points)
        elif len(mass) != len(points):
            raise ValueError("The lengths of mass and points should be the same")
        self.mass = defaultdict(int)
        self._diagonal = PDPoint([0,0])
        for i, p in enumerate(points):
            self.add(PDPoint(p), mass[i])
    
    def points(self):
        """
        Return a list of points in the diagram.
        """
        return list(self.mass)

    def add(self, point: PDPoint, mass: int = 1):
        """
        Add a point to the diagram with multiplicity.
        """
        if point.isdiagonalpoint():
            point = self._diagonal
        self.mass[point] += mass
        if self.mass[point] <= 0:            
            self.remove(point)

    def remove(self, point: PDPoint):
        """
        Remove a point from the diagram.
        """
        if point in self:
            del self.mass[point]
        else:
            raise KeyError("Point is not in the diagram")
    
    def clear(self):
        """
        Remove all points from the diagram.
        """
        self.mass.clear()

    def get_point_mass_lists(self):
        """
        Returns a tuple of lists.
        The first list contains all points in the diagram in PDPoint format.
        The second list contains all corresponding multiplicities.
        
        Note: The diagonal is ignored.
        """
        points = []
        masses = []
        for p in self.mass:
            if p != self._diagonal:
                points.append(p)
                masses.append(self.mass[p])
        return points, masses

    def loadfromfile(self,filename:str):
        """
        Clears current diagram and loads a diagram from a text file.
        Format for ith line:
        b_i d_i; mass_i
        where (b_i, d_i) is the ith point in the diagram with
        multiplicity mass_i.
        """
        self.clear()
        with open(filename, 'r') as d:
            for line in d:
                point, mass = line.rstrip().split("; ")
                self.add(PDPoint.fromstring(point), int(mass))

    def savetofile(self, filename:str = "diagram.txt"):
        """
        Save current diagram to a text file.
        Format for ith line:
        b_i d_i; mass_i
        where (b_i, d_i) is the ith point in the diagram with
        multiplicity mass_i.
        """
        with open(filename, 'w') as d:
            for p in self:
                d.write("; ".join([str(p), str(self.mass[p])])+"\n")

    def __iter__(self):
        return iter(self.mass)

    def __len__(self):
        """
        Note: The diagonal is ignored when computing the length
        """
        if self._diagonal in self.mass:
            return len(self.mass)-1
        else:
            return len(self.mass)

    def __contains__(self, point: PDPoint):
        return point in self.mass

    def __eq__(self, other):
        return self.mass == other.mass