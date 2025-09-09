from greedypermutation.maxheap import MaxHeap
from greedypermutation.neighborgraph import GreedyNeighborGraph, Cell
from metricspaces import metric_class, MetricSpace
from pdsketch import Diagram
from pdsketch.pdpoint import PDPoint
from math import inf
from collections import defaultdict

def persistence_greedy(D: Diagram, mass: tuple = ()):
    points = []
    masses = []
    point_set = set()
    for i, p in enumerate(D):
        diag = p.diagproj()
        if diag not in point_set:
            points.append(diag)
            point_set.add(diag)
            masses.append(0)
        if p not in point_set:
            points.append(p)
            point_set.add(diag)
            masses.append(mass[i])
    G = PersistenceNeighborGraph(MetricSpace(points), masses)
    yield from _greedy(points, G)


def _greedy(points, G):
    H = G.heap
    root = H.findmax()

    # Yield the first point.
    yield root.center, None, {root.center: G.cellmass(root)}

    for _ in range(1, len(points)):
        cell = H.findmax()
        point = cell.farthest
        _, transportplan = G.addcell(point, cell)
        yield point, cell.center, transportplan

@metric_class
class PersistenceCell:
    def __init__(self, center):
        self.points = {center}
        self.center = center
        self.radius = 0
        # super().__init__(center)

        self.diag_cell = True if center.isdiagonalpoint() else False
        if self.diag_cell:
            self.diag_points = {center}
            self.diag_left = center
            self.diag_right = center

    def addpoint(self, p):
        self.points.add(p)
        d = self.dist(p)
        if d > self.radius:
            self.radius = d
            self.farthest = p
        # super().addpoint(p)
        
        if self.diag_cell and p.isdiagonalpoint():
            self.diag_points.add(p)
            if p[0] < self.diag_left[0]:
                self.diag_left = p
            if p[0] > self.diag_right[0]:
                self.diag_right = p


    def dist(self, point):
        return self.center.proj_dist(point)
        
    def seg_dist(self, point):
        if self.center.isdiagonalpoint():
            d = point.diagproj()
            a = (point.dist(d) if self.diag_left[0] <= d[0] <= self.diag_right[0]
                 else min(point.l_inf_dist(self.diag_left), point.l_inf_dist(self.diag_right)))
        else:
            a = self.center.l_inf_dist(point)
        return a

    def comparedist(self, point, other):
        return self.seg_dist(point) < other.seg_dist(point)

    def update_diag(self):
        self.diag_left = (inf, inf)
        self.diag_right = (0,0)
        for p in self.diag_points:
            if p[0] < self.diag_left[0]:
                self.diag_left = p
            if p[0] > self.diag_right[0]:
                self.diag_right = p

    # Following methods can be commented. Same as parent's
    def updateradius(self):
        max_dist = 0
        max_point = None
        for p in self.points:
            d = self.dist(p)
            if d > max_dist:
                max_dist = d
                max_point = p
        self.radius = max_dist
        self.farthest = max_point

    def __len__(self):
        return len(self.points)

    def __iter__(self):
        return iter(self.points)

    def __contains__(self, point):
        return point in self.points

    def __lt__(self, other):
        return self.radius > other.radius

    def __repr__(self):
        return str(self.center)

class PersistenceNeighborGraph(GreedyNeighborGraph):
    def __init__(self, M, mass=None):
        super().__init__(M, nbrconstant=2, cell=PersistenceCell)
        if mass is None:
            mass = [1]*len(M)
        elif len(mass) != len(M):
            raise ValueError("`mass` must of same length as `M`")
        self.mass = defaultdict(int)
        for i, p in enumerate(M):
            self.mass[p] += mass[i]

    def addcell(self, newcenter, parent):
        """
        Add a new cell centered at `newcenter` and also compute the mass moved
        by this change to the neighbor graph.

        The `parent` is a sufficiently close cell that is already in the
        graph.
        It is used to find nearby cells to be the neighbors.
        The cells are rebalanced with points moving from nearby cells into
        the new cell if it is closer.

        If self.gettransportplan=True this method also returns a dictionary
        of the number of points gained and lost by every cell (indexed by
        center) in this change to the neighbor graph.
        """
        # Create transportation plan for adding this cell
        transportplan = defaultdict(int)
        
        # Create the new cell.
        newcell = self.Vertex(newcenter)

        # Make the cell a new vertex.
        self.addvertex(newcell)
        self.addedge(newcell, newcell)

        # Rebalance the new cell.
        for nbr in self.nbrs(parent):
            localtransport = self.rebalance(newcell, nbr)
            # Add change caused by this rebalance to transportation plan if
            # requested.
            if localtransport != 0:
                transportplan[newcenter] += localtransport
                transportplan[nbr.center] -= localtransport

            # The heap update has been delegated to the GreedyNeighborGraph.
            # self.heap.changepriority(nbr)

        # Add neighbors to the new cell.
        for newnbr in self.nbrs_of_nbrs(parent):
            if self.iscloseenoughto(newcell, newnbr):
                self.addedge(newcell, newnbr)

        # After all the radii are updated, prune edges that are too long.
        for nbr in set(self.nbrs(parent)):
            self.prunenbrs(nbr)

        self.heap.insert(newcell)

        return newcell, transportplan

    def rebalance(self, a, b):
        """
        Returns the number of points moved from `b` to `a`.

        Move points from the cell `b` to the cell `a` if they are
        sufficiently closer to `a.center`.
        """
        mass_to_move = 0
        if a.diag_cell and b.diag_cell:
            # move diagonal points first
            diag_to_move = {p for p in b.diag_points if a.center.l_inf_dist(p) < b.center.l_inf_dist(p)}
            b.points -= diag_to_move
            b.diag_points -= diag_to_move
            for p in diag_to_move:
                a.addpoint(p)
                mass_to_move += self.mass[p]
            b.update_diag()

        points_to_move = {p for p in b.points if a.comparedist(p, b)}
        b.points -= points_to_move
        for p in points_to_move:
            a.addpoint(p)
            mass_to_move += self.mass[p]
        # The radius of self (`a`) is automatically updated by addpoint.
        # The other radius needs to be manually updated.
        b.updateradius()
        self.heap.changepriority(b)
        return mass_to_move

    def iscloseenoughto(self, p: PersistenceCell, q: PersistenceCell):
        """
        Return True iff the cells `p` and `q` are close enough to be neighbors.
        """
        return (q.center.dist(p.center) <= p.radius + q.radius +
                                max(p.radius, q.radius)*self.nbrconstant)
    
    def cellmass(self, cell):
        """
        Method to compute the number of points with multiplicity in a cell.
        Better to use this than `len(cell)`.
        """
        return sum(self.mass[p] for p in cell)