# Draw Rips Complex

``` python {cmd="python3" output="html"}
from ds2viz.canvas import Canvas
import dionysus as d
import numpy as np
from ds2.graph import Graph
from ds2viz.datastructures import VizGraph
from ds2viz.canvas import Canvas
from itertools import combinations

class Rips:
    def __init__(self, points):
        self.points = points

    def draw(self, k, max_radius, incr=0.1):
        radius = 0
        prev_hash = (None, None)
        while radius < max_radius:
            filteration = d.fill_rips(self.points, k, radius)
            radius += incr
            V, E = set(), list()
            for simplex in filteration:
                V.update(set(simplex))
                E.extend(combinations(list(simplex), 2))
            if len(E) == 0:
                continue
            V = {str(v): tuple(self.points[v]) for v in V}
            E = {str(x)+str(y) for x,y in E}
            curr_hash = (hash(frozenset(V)), hash(frozenset(E)))
            if prev_hash == curr_hash:
                continue
            else:
                prev_hash = curr_hash
            G = Graph(V, E)
            vizG = VizGraph(G, V)
            canvas = Canvas(260, 260)
            vizG.draw(canvas)
            print(canvas.svgout())

points = np.array([[90,10], [100,100], [10,100], [10,10]], dtype='float64')
rips = Rips(points)
rips.draw(3, 350, 10)
```
