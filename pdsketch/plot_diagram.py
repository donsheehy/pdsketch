from pdsketch import Diagram, PDPointViz, PDPoint
from ds2viz.element import Line
from ds2viz.canvas import svg_plus_pdf
from pdsketch.sketch_style import sketch_style

def plot_diagram(diagram: Diagram, M: int = 0, filename: str = "diagram"):
    """
    Method to visualize a diagram.
    
    Parameters
    ----------
    diagram : Diagram
        The diagram to be plotted.
    M : int
        Size of the persistence plane to be plotted.
    filename : str
        Name of file to save output.
    """
    # Compute `M` if not given
    diagonal = PDPoint([0,0])
    if not M:
        M = max(p[1] for p in diagram)+5
    with svg_plus_pdf(M, M, filename, sketch_style) as canvas:
        # Draw points in the diagram using modified coordinates.
        # If point is diagonal then draw it in the center of the diagonal.
        [PDPointViz(p[0], M-p[1], diagram.masses[p]).draw(canvas) if p != diagonal 
            else PDPointViz(M//2, M//2, diagram.masses[p]).draw(canvas) for p in diagram]
        
        # Draw remaining borders of the bounded persistence plane.
        Line((0,M), (M,0)).draw(canvas)
        Line((0,0), (M,0)).draw(canvas)
        Line((M,0), (M,M)).draw(canvas)
        Line((M,M), (0,M)).draw(canvas)
        Line((0,M), (0,0)).draw(canvas)