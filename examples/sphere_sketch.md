# Why Sketching?

In many real-world situations persistence diagrams have a large number of points.
However, it is possible that even a few points can sufficiently explain the topology of the underlying space.
Despite providing little useful information additional points increase the bottleneck distance computation greatly.
Sketching provides a useful way to approximate a persistence diagrams while preserving the distribution of points.

``` python {cmd=true, hide}
from ds2viz.canvas import svg_plus_pdf
from ds2viz.element import Circle, Line
from pdsketch.pdpoint import PDPoint
from tadasets import sphere, torus
from ripser import ripser
from pdsketch import Diagram, Sketch, plot_sketch
from pdsketch.sketchpoint import SketchPoint
from pdsketch.sketch_style import sketch_style
```

Consider the following persistence diagram obtained by sampling points from a sphere.

```python{cmd, continue, output=html}
N = 5000
n = 20

sample = sphere(n=N, r=1000)
D = Diagram(ripser(sample)["dgms"][1])
sketch_n = [PDPoint(p) for p in D]

M = max(p[1] for p in sketch_n)+5

with svg_plus_pdf(M, M, "sphere_pd", sketch_style) as canvas:
    for p in sketch_n:
        innercircle = Circle(1, style='_circle', stylesheet=sketch_style)
        innercircle.align('center', (p[0], M-p[1]))
        innercircle.draw(canvas)
    Line((0,M), (M,0)).draw(canvas)
    Line((0,0), (M,0)).draw(canvas)
    Line((M,0), (M,M)).draw(canvas)
    Line((M,M), (0,M)).draw(canvas)
    Line((0,M), (0,0)).draw(canvas)
```
Using a sketch `i` we can represent an `n`-point persistence diagram using only `i` distinct points with total mass `n`.
Here we show sketches 5, 10  and 15 of this persistence diagram.
The point with the greatest persistence is the essence of this diagram and it is captured in each sketch.

```python{cmd, continue, output = markdown}
S = Sketch(D, n)

plot_sketch(S[5], filename="sphere_sketch_5")
plot_sketch(S[10], filename="sphere_sketch_10")
plot_sketch(S[15], filename="sphere_sketch_15")
```