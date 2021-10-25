from metricspaces import MetricSpace
from greedypermutation.greedytree import GreedyTree

class QuotientSpace(MetricSpace):
    """
    A class to store quotients of metric spaces with a single equivalence class.
    """

    def __init__(self, X:MetricSpace, Y:MetricSpace):
        """
        Initialize a new QuotientSpace object.
        """
        super().__init__(points=X.points, dist=X.dist, cache=X.cache, turnoffcache=X.turnoffcache)
        #self.checkYinX()
        self.tree = GreedyTree(Y)
        # Initialize dictionary to store nearest neighbors. SHOULD THIS BE LAZY?
        # Making it lazy allows use of this space with infinite MetricSpaces

        # self.nn = dict()
        # for a in X:
        #     self.nn[a] = tree.nn(a)    
        
    def proj(self, a):
        return super().dist(a, self.getNN(a))

    def dist(self, a, b):
        return min(super().dist(a, b), self.proj(a)+self.proj(b))

    def checkYinX():
        pass

    def comparedist(self, x, a, b, alpha):
        pass

    def getNN(self, x):
        return(self.tree.nn(x))