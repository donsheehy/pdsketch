# Draw a persistence diagram and its matching

First, we draw a persistence diagram.

``` python {cmd=true output="html"}
from ds2viz.canvas import Canvas
from pdsketch import Diagram, DiagramViz, sketch_style
A = Diagram([[20,300],[40,70]])
Aviz = DiagramViz(A, plot_size=400)

canvas = Canvas(400, 400, sketch_style.sketch_style)
Aviz.draw_skeleton(canvas)
Aviz.draw_points(canvas)

print(canvas.svgout())
```
