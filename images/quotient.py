"""
Draw a finite quotient space and ball using Pycairo.
"""

from metricspaces import MetricSpace
from pdsketch import QuotientSpace, PDPoint
from pdsketch.distance import l_inf
from greedypermutation import GreedyTree
import cairo as cr
from cairo import Context as ctx, Format, PDFSurface as pdf, ImageSurface as img

class FiniteQuotient(MetricSpace):
    """
    A class to represent points in $(\R^2, \l_\infty)$ with a finite quotient `Y`.
    """

    def __init__(self, Y:MetricSpace):
        super().__init__(dist=l_inf)
        self.tree = GreedyTree(Y)
        
    def proj(self, a):
        """
        Compute the distance between `a` and the projection of `a` on `Y`.
        """
        return super().dist(a, self.getNN(a))

    def dist(self, a, b):
        """
        Quotient distance between `a` and `b`.
        """
        return min(super().dist(a, b), self.proj(a)+self.proj(b))

    def getNN(self, x):
        """
        Compute the projection of `a` in the quotient.
        """
        return self.tree.nn(x)

def inch_to_point(x):
    return x*72.0

# target = pdf(None, inch_to_point(10), inch_to_point(10))
target = img(cr.Format.RGB24, 1000, 1000)
ctx = ctx(target)

ctx.rectangle(50,50,100,100)

# img.write_to_png(cr.Path("./output.png"))
img.write_to_png()