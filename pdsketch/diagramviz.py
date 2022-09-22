from pdsketch import Diagram, PDPoint
from pdsketch.pdpointviz import PDPointViz
from ds2viz.element import Line
from ds2viz.canvas import svg_plus_pdf
from pdsketch.sketch_style import sketch_style

class DiagramViz():
    """
    Class to depict a persistence diagram using ds2viz.
    Stores PDPoints of a diagram as PDPointViz objects and draws them when asked to.
    """
    def __init__(self, diagram:Diagram, style:str = None, plot_size:int = 0):
        """
        Parameters
        ----------
        diagram : Diagram
            The PD to be plotted
        style : str
            Important only when plotting bottleneck matchings
        plot_size : int
            Important only when plotting bottleneck matchings
        """
        self.plot_size = max(p[1] for p in diagram)+5 if not plot_size else plot_size
        self.points = [PDPointViz(p, diagram.mass[p], self.plot_size, style) for p in diagram]

    def draw_skeleton(self, canvas):
        # Draw diagonal and boundaries of persistence diagram
        Line((0,self.plot_size), (self.plot_size,0), style='_diagonal', stylesheet=sketch_style).draw(canvas)
        Line((0,0), (self.plot_size,0), style='_boundary', stylesheet=sketch_style).draw(canvas)
        Line((self.plot_size,0), (self.plot_size,self.plot_size), style='_boundary', stylesheet=sketch_style).draw(canvas)
        Line((self.plot_size,self.plot_size), (0,self.plot_size), style='_boundary', stylesheet=sketch_style).draw(canvas)
        Line((0,self.plot_size), (0,0), style='_boundary', stylesheet=sketch_style).draw(canvas)
        
    def draw_points(self, canvas):
        # Draw points of the persistence diagrame
        [p.draw(canvas) for p in self.points]

    def draw(self, filename:str):
        # Draw both, points and boundaries
        with svg_plus_pdf(self.plot_size, self.plot_size, filename, sketch_style) as canvas:
            self.draw_skeleton(canvas)
            self.draw_points(canvas)