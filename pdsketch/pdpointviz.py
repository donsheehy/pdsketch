from matplotlib.pyplot import plot
from pdsketch import PDPoint
from ds2viz.element import Circle, Text
from pdsketch.sketch_style import sketch_style

class PDPointViz():
    """
    Class to depict a point in a sketch.
    Mainly used to visualize a sketch.
    A point in a sketch is a PDPoint (point in a PD) and some mass.
    """
    
    def __init__(self, p:PDPoint, mass:int, plot_size:int , style:str='_circle'):
        self.point = [p[0], plot_size-p[1]]
        self.mass = mass
        self.style = style

    def draw(self, canvas):
        # Create mass label for a point in a sketch and draw it.
        # !!!! Needs a change in ds2viz to run.
        # element.py line 130: change `super().__init__()` to `super().__init__(style, stylesheet)`
        # Have also changed line 134 to modify size of textbox from 17* to 10*
        label = Text(str(self.mass), style='_text', stylesheet=sketch_style)
        label.align('left', (self.point[0], self.point[1]))
        label.draw(canvas)

        # Draw a point in a sketch as 2 concentric circles.
        point = Circle(1, style=self.style, stylesheet=sketch_style)
        point.align('center', (self.point[0], self.point[1]))
        point.draw(canvas)
