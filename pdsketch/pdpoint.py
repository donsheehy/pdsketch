class PDPoint:
    """
    A class to describe points in the persistence plane.
    """
        
    def __init__(self, coords):
        """
        Parameters
        ----------
        coords: tuple
            The coordinates of the point
            The tuple must contain two float coordinates such that the second coordinate is at least as great as the first.
        """
        if len(coords)!=2:
            raise TypeError("Invalid points input. Points in the persistence plane are 2D")
        if coords[0] > coords[1]:
            print(coords)
            raise ValueError("Birth value cannot be greater than death value")
        self._p = tuple(float(x) for x in coords)

    @staticmethod
    def fromstring(s):
        """
        Return a new point object from a string representation.
        """
        return PDPoint([float(x) for x in s.split()])

    def dist(self, other) -> float:
        # The reason this exists as a copy of `self.pp_dist` is to allow easy swapping over to `self.l_inf_dist` if needed.
        """
        Compute quotient distance in the persistence plane.
        The diagonal is treated as a single point.
        """
        return self.pp_dist(other)

    def diagproj(self):
        """
        Compute the projection of this point on the diagonal.
        """
        return PDPoint([(self[0]+self[1])/2, (self[0]+self[1])/2])

    def pp_dist(self, other)->float:
        """
        Compute quotient distance in the persistence plane.
        The diagonal is treated as a single point.
        """
        return min(self.l_inf_dist(other), self.l_inf_dist(self.diagproj())+other.l_inf_dist(other.diagproj()))
    
    def l_inf_dist(self, other)->float:
        """
        Compute the l_inf distance between the `self` and `other`.
        If the dimensions don't match the distance is computed in projection
        down to the common subspace.
        """
        return max(abs(a-b) for (a,b) in zip(self, other))
        
    def isdiagonalpoint(self)->bool:
        """
        Check if this point lies on the diagonal.
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