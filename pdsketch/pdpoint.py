class PDPoint:
    """
    A simple class to describe points in Euclidean space with float
    coordinates.
    """
        
    def __init__(self, coords, mult=1):
        if len(coords)!=2:
            raise TypeError("Invalid points input. Points in persistence plane are 2D")
        if coords[0] > coords[1]:
            raise ValueError("Birth value cannot be greater than death value in the"+
                                " persistence plane")
        self._p = tuple(float(x) for x in coords)
        self.mass = mult

    @staticmethod
    def fromstring(s):
        """
        Return a new point object from a string representation.
        """
        return PDPoint([x for x in s.split()])

    def dist(self, other) -> float:
        """Compute the l_inf distance between the `self` and `other`.
        If the dimensions don't match the distance is computed in projection
        down to the common subspace.
        """
        return max(abs(a-b) for (a,b) in zip(self, other))

    def diagproj(self):
        """
        Compute the projection of this point on the diagonal.
        """
        return PDPoint([(self[0]+self[1])/2, (self[0]+self[1])/2], self.mass)

    def pp_dist(self, other)->float:
        """
        Compute quotient distance in the persistence plane.
        The diagonal is treated as a single point.
        """
        return min(self.dist(other), self.dist(self.diagproj())+other.dist(other.diagproj()))
    
    def isdiagonalpoint(self)->bool:
        """
        Check if this is a diagonal point.
        """
        return self[0]==self[1]

    def __getitem__(self, index):
        return self._p[index]

    def __eq__(self, other):
        return self._p == other._p

    def __hash__(self):
        return hash(self._p)

    def __str__(self):
        return " ".join(str(c) for c in self._p)

    def __iter__(self):
        return iter(self._p)

    def __len__(self):
        return len(self._p)

    def __repr__(self):
        return str(self)