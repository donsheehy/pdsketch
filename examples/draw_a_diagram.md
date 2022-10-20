# Draw a persistence diagram and its matching

First, we draw a persistence diagram.

``` python {cmd=true output="html"}
from ds2viz.canvas import Canvas
from pdsketch import Diagram
from pdsketch.vizdiagram import VizDiagram
from pdsketch.sketch_style import sketch_stylesheet

A = Diagram.load_from_file("sphere_1000.dgm")
B = Diagram.load_from_file("sphere_1000.dgm") # Change
# b_stylesheet = load ...

"""
B = Diagaram ... # To merge together
C = Diagaram ... # To merge together
"""

# print(sketch_stylesheet.styles)

Aviz = VizDiagram(A, style='pd_graph', stylesheet=sketch_stylesheet, plot_size=400)
# Bviz = VizDiagram(B, style='pd_graph_b', stylesheet=sketch_stylesheet, plot_size=400)

vizList = [Aviz]

# Get max
max = 400

canvas = Canvas(max, max, sketch_stylesheet)
# Aviz.draw(canvas)
for viz in vizList:
    viz.draw(canvas)

# Aviz.draw_points(canvas)

print(canvas.svgout())
```
