# Draw Rips Complex

``` python {cmd="python3" output="html"}
from ds2viz.canvas import Canvas
from ds2viz.element import Group, Element, Box, Circle
import dionysus as d
import numpy as np
from ds2.graph import Graph
from ds2viz.datastructures import VizGraph
from ds2viz.canvas import Canvas
from itertools import combinations
from pdsketch.sketch_style import sketch_style

class Polygon(Element):
    def __init__(self, points, stylesheet, style='_polygon'):
        super().__init__(style, stylesheet)
        x_coords, y_coords = zip(*points)
        self.points = points
        self._box = Box(min(y_coords), max(x_coords), max(y_coords), min(x_coords))
    
    def draw(self, canvas):
        # TODO: add anchors
        canvas.polygon(self.points, self.style)

class VizRipsGraph(Group):
    def __init__(self, vertices, polygons, points, stylesheet):
        super().__init__()
        for polygon in polygons:
            edges = list()
            for a,b in polygon:
                edges.extend([points[int(a)], points[int(b)]])
            edges = set([tuple(x) for x in edges])
            edges = [np.array(x) for x in edges]
            if len(edges) == 2:
                stylesheet.styles["_polygon"][0]['stroke'] = (0,0,0)
            self.addelement(Polygon(edges, stylesheet))

        for v in vertices:
            c = Circle(3)
            c.align('center', points[int(v)])
            self.addelement(c)

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
                edges = list(combinations(list(simplex), 2))
                if edges != list():
                    E.append(edges)
            if len(E) == 0:
                continue
            V = {str(v): tuple(self.points[v]) for v in V}
            E = {tuple(str(x)+str(y) for x,y in edges) for edges in E}
            curr_hash = (hash(frozenset(V)), hash(frozenset(E)))
            if prev_hash == curr_hash:
                continue
            else:
                prev_hash = curr_hash
            vizG = VizRipsGraph(V, E, self.points, sketch_style)
            canvas = Canvas(150, 150, sketch_style)
            vizG.draw(canvas)
            print(canvas.svgout())

# canvas = Canvas(150, 150, sketch_style)
# canvas.polygon([(100,10), (10,100), (10, 10), (10, 10)])
# print(canvas.svgout())

points = np.array([[90,10], [100,100], [10,100], [10,10], [120, 120]], dtype='float64')
# points = np.array([[100,10], [100,100], [10,100], [10,10]], dtype='float64')
rips = Rips(points)
rips.draw(3, 350, 10)
```
