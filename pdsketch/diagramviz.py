from pdsketch import Diagram, PDPoint
from pdsketch.pdpointviz import PDPointViz
from ds2viz.element import Line
from pdsketch.sketch_style import sketch_stylesheet

"""
Reduce redundancy in the canvas in draw()
"""

class DiagramViz():
    """
    Class to depict a persistence diagram using ds2viz.
    Stores PDPoints of a diagram as PDPointViz objects and draws them when asked to.
    """
    def __init__(self, diagram:Diagram, draw_labels:bool=True, style:str = None, plot_size:int = 0):
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
        self.points = [PDPointViz(p, diagram.mass[p], self.plot_size, draw_labels, style) if not p.isdiagonalpoint() else PDPointViz(PDPoint((self.plot_size//2, self.plot_size//2)), diagram.mass[p], self.plot_size, draw_labels, style) for p in diagram]

    def draw(self, canvas):
        # Draw diagonal and boundaries of persistence diagram
        Line((0,self.plot_size), (self.plot_size,0), style='_diagonal', stylesheet=sketch_stylesheet).draw(canvas)
        Line((0,0), (self.plot_size,0), style='_boundary', stylesheet=sketch_stylesheet).draw(canvas)
        Line((self.plot_size,0), (self.plot_size,self.plot_size), style='_boundary', stylesheet=sketch_stylesheet).draw(canvas)
        Line((self.plot_size,self.plot_size), (0,self.plot_size), style='_boundary', stylesheet=sketch_stylesheet).draw(canvas)
        Line((0,self.plot_size), (0,0), style='_boundary', stylesheet=sketch_stylesheet).draw(canvas)

        # Draw points of the persistence diagram
        for p in self.points:
            p.draw(canvas)