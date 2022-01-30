from pdsketch import PDPoint
from ds2viz.element import Circle, Text
from pdsketch.sketch_style import sketch_style

class PDPointViz():
    """
    Class to depict a point in a sketch.
    Mainly used to visualize a sketch.
    A point in a sketch is a PDPoint (point in a PD) and some mass.
    """
    # def __init__(self, point:PDPoint, mass:int):
    #     # super().__init__(radius)
    #     self.point = point
    #     self.mass = mass
    #     # self.align('center', (point[0], point[1]))
    
    def __init__(self, x, y, mass):
        self.point = [x, y]
        self.mass = mass

    def draw(self, canvas):
        # Create mass label for a point in a sketch and draw it.
        # !!!! Needs a change in ds2viz to run.
        # element.py line 130: change `super().__init__()` to `super().__init__(style, stylesheet)`
        label = Text(str(self.mass), style='_text', stylesheet=sketch_style)
        label.align('left', (self.point[0], self.point[1]))
        label.draw(canvas)

        # Draw a point in a sketch as 2 concentric circles.
        outercircle = Circle(4, style='_circle', stylesheet=sketch_style)
        outercircle.align('center', (self.point[0], self.point[1]))
        outercircle.draw(canvas)

        innercircle = Circle(1, style='_circle', stylesheet=sketch_style)
        innercircle.align('center', (self.point[0], self.point[1]))
        innercircle.draw(canvas)
