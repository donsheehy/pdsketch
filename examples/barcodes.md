# Draw a barcode

``` python {cmd="python3" output="html"}
from ds2viz.canvas import Canvas
from pdsketch import Diagram
from ds2viz.element import Line
from pdsketch.sketch_style import sketch_style
import seaborn as sns
diagram = Diagram.load_from_file('./sphere_1000.dgm')

class Barcodes:
    def __init__(self, diagram: Diagram):
        self.plot_size = max(coord[1] for coord in diagram)

    def draw(self, canvas: Canvas, sort_by_birth=True, cuts=None, color_scheme="rocket"):
        cuts.insert(0, 0)
        cuts.append(self.plot_size)
        colors = sns.color_palette(color_scheme, len(cuts)-1)
        cuts_range = [(cuts[i-1], cuts[i], colors[i-1]) for i in range(1, len(cuts))]

        # Drawing axes
        Line((0, self.plot_size), (0, 0), '_boundary', sketch_style).draw(canvas)
        Line((self.plot_size, self.plot_size), (0, self.plot_size), '_boundary', sketch_style).draw(canvas)

        # Drawing bars
        width_from_bottom = 5
        y = self.plot_size - width_from_bottom
        spacing = (self.plot_size)/len(diagram)
        for coord in sorted(diagram, key=lambda x: x[int(not sort_by_birth)]):
            start, end = coord[0], coord[1]
            for cut_start, cut_end, color in cuts_range:
                sketch_style.styles["_line"][0]['stroke'] = color
                if start <= cut_start and cut_end >= end and cut_start <= end:
                    Line((cut_start, y), (end, y), '_line', sketch_style).draw(canvas)
                elif start >= cut_start and cut_end <= end and start <= cut_end:
                    Line((start, y), (cut_end, y), '_line', sketch_style).draw(canvas)
                elif start < cut_start and cut_end < end:
                    Line((cut_start, y), (cut_end, y), '_line', sketch_style).draw(canvas)
                elif start > cut_start and cut_end > end:
                    Line((start, y), (end, y), '_line', sketch_style).draw(canvas)
            y -= spacing

barcodes = Barcodes(diagram)
cuts = [barcodes.plot_size/3, 2*barcodes.plot_size/3]
canvas = Canvas(barcodes.plot_size, barcodes.plot_size, sketch_style)
barcodes.draw(canvas, sort_by_birth=True, cuts=cuts)
print(canvas.svgout())
```
