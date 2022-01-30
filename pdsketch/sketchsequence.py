from collections import defaultdict
from metricspaces import MetricSpace
from pdsketch import Diagram, PDPoint
from greedypermutation.clarksongreedy import greedy

class SketchSequence:
    """
    A class to generate sketches from a persistence diagram.
    """
    def __init__(self, diagram: Diagram, n: int = None):
        """
        Parameters
        ----------
        diagram : Diagram
            The PD to be sketched
        n : int
            The number of sketches to be produced
        """
        if not n:
            n = len(diagram)     
        
        points, masses = diagram.get_point_mass_lists()
        total_mass = sum(masses)
        diagonal = PDPoint([0,0])
        # Adding the diagonal with a multiplicity of `total_mass`
        points.append(diagonal)
        masses.append(total_mass)
        sketches = greedy(M=MetricSpace(points), seed=diagonal, nbrconstant=2, tree=True, gettransportplan=True, mass=masses)
        
        i = 0
        self._sketches = []
        while i <= n:
            point, parent_index, transport_plan = next(sketches)
            if i == 0 or not point.isdiagonalpoint():
                # The above condition ensures that only off-diagonal points are added to the sketch except for the 0th sketch which is just the diagonal.
                self._sketches.append({'point':point, 'parent_index': parent_index, 'transport_plan': transport_plan.copy()})
                i += 1
        # Remove the diagonal projections from the zeroth sketch            
        self._sketches[0]['transport_plan'][diagonal] -= total_mass

    def sketch_bottleneck(self, i:int)->float:
        """
        Returns the bottleneck distance between the original diagram and its ith sketch
        """
        if i < len(self._sketches)-1:
            return self._sketches[i+1]['point'].dist(self._sketches[self._sketches[i+1]['parent_index']]['point'])
        else:
            return None
        
    def _to_dict(self, str_transport: str):
        """
        Internal method to convert string to transportation plan.
        Used only in method `loadfromfile()`.
        """
        transport = defaultdict(int)
        str_transport = str_transport[str_transport.find('{')+1:str_transport.find('}')]
        dict_entries = str_transport.split(", ")
        for entry in dict_entries:
            key_value = entry.split(": ")
            transport[PDPoint([float(p) for p in key_value[0].split()])] = int(key_value[1])
        return transport
    
    def loadfromfile(self, filename:str):
        """
        Clears current sketches and loads sketches from a text file.
        File format:
        b_i d_i; parent_i; transportplan_i
        where (b_i, d_i) is the ith point added to the sketch, parent_i is its parent
        and transportplan_i is the ith transportation plan in defaultdict(int) format.
        """
        self._sketches.clear()
        with open(filename, 'r') as s:
            for sketch in s:
                point, parent, transport = sketch.rstrip().split("; ")
                point = PDPoint.fromstring(point)
                parent_index = int(parent) if parent != 'None' else None
                transport = self._to_dict(transport)
                self._sketches.append({'point':point, 'parent_index': parent_index, 'transport_plan': transport})

    def savetofile(self, filename:str = "sketch"):
        """
        Save current sketches to a text file.
        The ith line will be saved as follows:
        b_i d_i; parent_i; transportplan_i
        where (b_i, d_i) is the ith point added to the sketch, parent_i is the index of its
        parent and transportplan_i is the ith transportation plan in defaultdict(int) format.
        """
        with open(filename, 'w') as s:
            for sketch in self._sketches:
                s.write("; ".join([str(sketch['point']), str(sketch['parent_index']), str(sketch['transport_plan'])])+"\n")

    def __getitem__(self, index:int)->defaultdict:
        sketch = Diagram()
        for i in range(index+1):
            for p in self._sketches[i]['transport_plan']:
                sketch.add(p, self._sketches[i]['transport_plan'][p])
        return sketch
    
    def __iter__(self):
        return iter(self._sketches)

    def __hash__(self) -> int:
        return hash(tuple(tuple(sketch) for sketch in self._sketches))