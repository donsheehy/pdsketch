from pdsketch import PDPoint
from ds2viz.element import Circle, Text
from pdsketch.sketch_style import sketch_style

class PDPointViz():
    """
    Class to depict a point in the persistence plane with mass using ds2viz. 
    """
    def __init__(self, p:PDPoint, mass:int, plot_size:int , style:str=None):
        """
        Parameters
        ----------
        p : PDPoint
            The point to be plotted
        mass : int
            The multiplicity of p
        plot_size : int
            The dimension of the plot.
            Needed to transform p's orientation.
        style : str
            Drawing style.
            Can be a particular diagram color.
        """
        self.point = [p[0], plot_size-p[1]]
        self.mass = mass
        self.style = style if style else '_circle'

    def draw(self, canvas):
        # !!!! Needs a change in ds2viz to run.
        # element.py line 130: change `super().__init__()` to `super().__init__(style, stylesheet)`
        # Have also changed line 134 to modify size of textbox from 17* to 10*
        
        # Create mass label for a point and draw it
        label = Text(str(self.mass), style='_text', stylesheet=sketch_style)
        label.align('left', (self.point[0], self.point[1]))
        label.draw(canvas)

        # Draw a point in a sketch as a circle
        point = Circle(1, style=self.style, stylesheet=sketch_style)
        point.align('center', (self.point[0], self.point[1]))
        point.draw(canvas)
