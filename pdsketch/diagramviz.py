from pdsketch import Diagram, PDPointViz, PDPoint
from ds2viz.element import Line
from ds2viz.canvas import svg_plus_pdf
from pdsketch.sketch_style import sketch_style

class DiagramViz():
    def __init__(self, d:Diagram, style:str = None, plot_size:int = 0):
        # self.style = '_circle' if not style else style
        self.plot_size = max(p[1] for p in d)+5 if not plot_size else plot_size
        self.points = [PDPointViz(p, d.mass[p], self.plot_size, style) for p in d]

    def draw_skeleton(self, canvas):
        Line((0,self.plot_size), (self.plot_size,0), style='_diagonal', stylesheet=sketch_style).draw(canvas)
        Line((0,0), (self.plot_size,0), style='_boundary', stylesheet=sketch_style).draw(canvas)
        Line((self.plot_size,0), (self.plot_size,self.plot_size), style='_boundary', stylesheet=sketch_style).draw(canvas)
        Line((self.plot_size,self.plot_size), (0,self.plot_size), style='_boundary', stylesheet=sketch_style).draw(canvas)
        Line((0,self.plot_size), (0,0), style='_boundary', stylesheet=sketch_style).draw(canvas)
        
    def draw_points(self, canvas):
        [p.draw(canvas) for p in self.points]

    def draw(self, filename:str):
        with svg_plus_pdf(self.plot_size, self.plot_size, filename, sketch_style) as canvas:
            self.draw_skeleton(canvas)
            self.draw_points(canvas)