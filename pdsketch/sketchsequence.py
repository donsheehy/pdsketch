from collections import defaultdict
from metricspaces import MetricSpace
from pdsketch import Diagram, PDPoint
from greedypermutation.clarksongreedy import greedy
from collections import namedtuple

SketchEntry = namedtuple('SketchEntry', ['point',
                                         'mass',
                                         'parent',
                                         'update_plan'])

class SketchSequence:
    """
    A class to generate sketches from a persistence diagram.
    """
    def __init__(self, diagram: Diagram = None, n: int = None):
        """
        Parameters
        ----------
        diagram : Diagram
            The PD to be sketched
        n : int
            The number of sketches to be produced
        """
        # If you want an empty sketch, you can have one.
        if diagram is None:
            self._sketches = []
            return

        if n is not None:
            n = len(diagram)

        points, masses = diagram.get_point_mass_lists()
        total_mass = diagram.total_mass
        diagonal = PDPoint([0,0])
        # Adding the diagonal with a multiplicity of 0.
        points.append(diagonal)
        masses.append(0)
        sketches = greedy(M=MetricSpace(points),
                          seed=diagonal,
                          tree=True,
                          gettransportplan=True,
                          mass=masses)

        # Handle the first point
        point, _, update_plan = next(sketches)
        # self._sketches = [SketchEntry(point, 0, None, {point: total_mass})]
        self._sketches = [SketchEntry(point, 0, None, update_plan)]

        # Handle the rest of the points.
        for point, parent, update_plan in sketches:
            mass = diagram.mass[point]
            self._sketches.append(SketchEntry(point, mass, parent, update_plan))
            if len(self._sketches) == n:
                return
        # i = 0
        # while i <= n:
        #     point, parent_index, transport_plan = next(sketches)
        #     if i == 0 or not point.isdiagonalpoint():
        #         # The above condition ensures that only off-diagonal points are added to the sketch except for the 0th sketch which is just the diagonal.
        #         self._sketches.append({'point':point, 'parent_index': parent_index, 'transport_plan': transport_plan.copy()})
        #         i += 1
        # Remove the diagonal projections from the zeroth sketch
        # self._sketches[0]['transport_plan'][diagonal] -= total_mass

    def sketch_bottleneck(self, i:int)->float:
        """
        Returns the bottleneck distance between the original diagram and its ith sketch
        """
        if i >= len(self._sketches) - 1:
            return 0
        else:
            s = self._sketches[i+1]
            parent = self._sketches[s.parent].point
            return s.point.dist(parent)
        # if i < len(self._sketches)-1:
        #     return self._sketches[i+1]['point'].dist(self._sketches[self._sketches[i+1]['parent_index']]['point'])
        # else:
        #     return None

    def _to_dict(str_transport: str):
        """
        Internal method to convert string to transportation plan.
        Used only in method `load_from_file()`.
        """
        transport = defaultdict(int)
        str_transport = str_transport[str_transport.find('{')+1:str_transport.find('}')]
        if str_transport == '':
            return transport
        dict_entries = str_transport.split(", ")
        for entry in dict_entries:
            point_string, mass = entry.split(": ")
            point = PDPoint.fromstring(point_string)
            transport[point] = int(mass)
        return transport

    def load_from_file(filename:str):
        """
        Loads a sketch sequence from a text file.
        File format:
        b_i d_i; parent_i; transportplan_i
        where (b_i, d_i) is the ith point added to the sketch, parent_i is its parent
        and transportplan_i is the ith transportation plan in defaultdict(int) format.
        """
        S = SketchSequence()
        with open(filename, 'r') as s:
            for sketch in s:
                point, mass, parent, update_plan = sketch.rstrip().split("; ")
                point = PDPoint.fromstring(point)
                mass = int(mass)
                parent = int(parent) if parent != 'None' else None
                update_plan = SketchSequence._to_dict(update_plan)
                S._sketches.append(SketchEntry(point, mass, parent, update_plan))
        return S

    def save_to_file(self, filename:str = "sketch.dgm"):
        """
        Save current sketches to a text file.
        The ith line will be saved as follows:
        b_i d_i; mass_i; parent_i; updateplan_i
        where (b_i, d_i) is the ith point added to the sketch, parent_i is the
        index of its parent and updateplan_i is the ith transportation plan as
        a dictionary.
        """
        with open(filename, 'w') as s:
            s.write(str(self))

    def __getitem__(self, index:int)->defaultdict:
        sketch = Diagram()

        for i in range(index+1):
            for p in self._sketches[i].update_plan:
                sketch.add(p, self._sketches[i].update_plan[p])
        return sketch

    def __iter__(self):
        return iter(self._sketches)

    def __len__(self) -> int:
        return len(self._sketches)

    def __str__(self):
        entries = []
        for point, mass, parent, update_plan in self._sketches:
            entries.append(f"{point}; {mass}; {parent}; {dict(update_plan)}")
        return "\n".join(entries)
