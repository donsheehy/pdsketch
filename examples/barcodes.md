# Draw a barcode

``` python {cmd="python3" output="html"}
from ds2viz.canvas import Canvas
from pdsketch import Diagram
from ds2viz.element import Line
from pdsketch.diagramviz import sketch_style
diagram = Diagram.load_from_file('./sphere_1000.dgm')

class Barcodes:
    def __init__(self, diagram: Diagram):
        self.plot_size = max(coord[1] for coord in diagram)

    def draw(self, canvas: Canvas, sort_by_birth=True):
        Line((0, self.plot_size), (0, 0), '_boundary', sketch_style).draw(canvas)
        Line((self.plot_size, self.plot_size), (0, self.plot_size), '_boundary', sketch_style).draw(canvas)

        width_from_bottom = 5
        y = self.plot_size - width_from_bottom
        spacing = (self.plot_size)/len(diagram)
        for coord in sorted(diagram, key=lambda x: x[int(not sort_by_birth)]):
            start, end = coord[0], coord[1]
            Line((start, y), (end, y), '_boundary', sketch_style).draw(canvas)
            y -= spacing

barcodes = Barcodes(diagram)
canvas = Canvas(barcodes.plot_size, barcodes.plot_size, sketch_style)
barcodes.draw(canvas)
print(canvas.svgout())
```
