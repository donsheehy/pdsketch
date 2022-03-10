from pdsketch import Diagram, DiagramViz
from ds2viz.canvas import svg_plus_pdf
from ds2viz.element import Line, Text
from pdsketch.sketch_style import sketch_style

def plot_matching(a: Diagram, b: Diagram, matching, bottleneck, filename):

    # Select larger of the two diagrams as base
    plot_size_a = max(p[1] for p in a)
    plot_size_b = max(p[1] for p in b)

    base = a if plot_size_a >= plot_size_b else b
    other = a if base == b else b

    base_viz = DiagramViz(base, style='_diagram_a')
    other_viz = DiagramViz(other, style='_diagram_b', plot_size = base_viz.plot_size)

    with svg_plus_pdf(base_viz.plot_size, base_viz.plot_size, filename, sketch_style) as canvas:
        base_viz.draw_skeleton(canvas)

        # Draw every line segment in the matching
        for p_a in matching:
            for p_b in matching[p_a]:
                match_style = '_bottleneck' if p_a.dist(p_b) == bottleneck else '_matching'
                mass = matching[p_a][p_b]

                x = p_b.diagproj() if p_a.isdiagonalpoint() else p_a
                y = p_a.diagproj() if p_b.isdiagonalpoint() else p_b

                Line((x[0], base_viz.plot_size-x[1]), (y[0], base_viz.plot_size-y[1]), style=match_style, stylesheet=sketch_style).draw(canvas)
                label = Text(str(mass), style='_match_mass', stylesheet=sketch_style)
                label.align('left', ((x[0]+y[0])/2-8, base_viz.plot_size - (x[1]+y[1])/2))
                label.draw(canvas)

        # Draw every point
        base_viz.draw_points(canvas)
        other_viz.draw_points(canvas)
