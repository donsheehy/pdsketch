from pdsketch import Diagram, PDPoint
from pdsketch.pdpointviz import PDPointViz
from ds2viz.element import Line, Group
from pdsketch.sketch_style import sketch_stylesheet

"""
See how Element and Canvas and Styles work
"""

class VizDiagram(Group):
    """
    Class to depict a persistence diagram using ds2viz.
    Stores PDPoints of a diagram as PDPointViz objects and draws them when asked to.
    """
    def __init__(self, diagram:Diagram, style='pd_graph', stylesheet=sketch_stylesheet, plot_size:int = 0):
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

        super().__init__([], style, stylesheet)
        # for s in sketch_stylesheet:
        #     print( s )

        self.style_dict = next(self.stylesheet[style])

        plot_size = max(p[1] for p in diagram)+5 if not plot_size else plot_size
        points = []
        for p in diagram:
            if not p.isdiagonalpoint():
                self.addelement(PDPointViz(p, diagram.mass[p], plot_size, False), 'circle')

        # Draw diagonal and boundaries of persistence diagram
        diagonal_style = self.style_dict['diagonal']
        boundary_style = self.style_dict['boundary']

        self.addelement(Line((0,plot_size), (plot_size,0)), diagonal_style)

        # corners = [(0,0), (plot_size,0), (plot_size,plot_size), (0,plot_size)]
        
        # Can be polygon instead
        self.addelement(Line((0,0), (plot_size,0)), boundary_style)
        self.addelement(Line((plot_size,0), (plot_size,plot_size)), boundary_style)
        self.addelement(Line((plot_size,plot_size), (0,plot_size)), boundary_style)
        self.addelement(Line((0,plot_size), (0,0)), boundary_style)

        # Draw points of the persistence diagram
        # for p in points:
        #     self.addelement(p)
