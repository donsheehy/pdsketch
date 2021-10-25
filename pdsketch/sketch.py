from collections import defaultdict
from pdsketch import Diagram, PDPoint
from greedypermutation.clarksongreedy import greedy

class Sketch:
    """
    A class to generate sketches from a persistence diagram.


    """
    def __init__(self, D: Diagram, n: int = 0, seed: PDPoint = None):     #What should be the seed for a sketch?
        """
        Parameters
        ----------
        D : Diagram
            The PD to be sketched
        n : int
            The number of sketches to be produced
        seed : PDPoint
            The starting PDPoint of the sketch
        """

        sketches = greedy(M=D, seed=seed or D[-1], nbrconstant=2, tree=True, gettransportplan=True)
        self._sketches = [next(sketches) for i in range(n)]
        self._state = {'index': 0, 'mass': defaultdict(int, self._sketches[0][2])}

    def __getitem__(self, index)->defaultdict:
        """
        Return sketch accessed by index.
        """
        # Different approach when slicing??
        if isinstance(index, slice):
            # return a generator which can iterate over the requested sketches
            indices = range(index.start, index.stop, index.step)
            return (self._sketches[i] for i in indices)
        else:
            # fetch self._sketches[index]
            sign = 1 if index >= self._state['index'] else -1
            while index != self._state['index']:
                self._updateState(sign)
            return self._state['mass']

    def __iter__(self):
        """
        Returns an iterator on the sketches.
        """
        return iter(self._sketches)

    def __hash__(self) -> int:
        return hash(tuple(self._sketches))

    def _updateState(self, sign):
        """
        Internal method to move from one sketch to another.
        Moves the current sketch in memory to one forward or backward depending on `sign`.
        """
        self._state['index'] += sign
        transport = self._sketches[self._state['index']][2]
        for p in transport:
            self._state['mass'][p] += sign*transport[p]
        
    def loadfromfile():
        pass

    def savetofile():
        pass