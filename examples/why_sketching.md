# Why Sketching?

In many real-world situations PDs have a large number of points.
However, it is possible that even a few points can sufficiently explain the topology of the underlying space.
Despite providing little useful information additional points increase the bottleneck distance computation greatly.
Sketching provides a useful way to approximate a PD while preserving the distribution of points.

## PD of Points Sampled from a Sphere
``` python {cmd=true, hide}
from ds2viz.canvas import Canvas
from pdsketch import PDPoint, Diagram, SketchSequence
from pdsketch.diagramviz import DiagramViz
from pdsketch.sketch_style import sketch_style
```
``` python {cmd=false, hide}
# ripsing stuff
# from ripser import ripser
# from tadasets import sphere
# sample = sphere(1000, r=1000)
# D = Diagram(ripser(sample)['dgms'][1])
# D.save_to_file('sphere_2.txt')
```
Consider the following 1-dimensional PD obtained by sampling 1000 points from a sphere of radius 1000.

```python{cmd, continue, id=d_define, output=html}
D = Diagram.load_from_file('sphere_2.dgm')
```
```python{cmd, continue=d_define,id=d_draw, output=html, hide}
M = max(p[1] for p in D)+5
canvas = Canvas(M, M, styles=sketch_style)
D_viz = DiagramViz(D, draw_labels=False)
D_viz.draw(canvas)
print(canvas.svgout())
```

## Sketching a PD
Using the `i`th sketch we can represent an `n`-point PD using only `i` distinct points with total mass `n`.
Here we show sketches 5, 10, 15 and 20 of `D`.
The points with the greatest persistence are the essence of this diagram and they are captured in each sketch.

```python{cmd, continue=d_define, output=html}
M = max(p[1] for p in D)+5
n = 21
S = SketchSequence(D, n)
sketches_to_draw = [5, 10, 15, 20]

for i in sketches_to_draw:
    D_i = S[i]
    D_i_viz = DiagramViz(D_i)
    canvas = Canvas(M, M, styles=sketch_style)
    D_i_viz.draw(canvas)
    print(canvas.svgout())
```