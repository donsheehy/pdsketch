from pdsketch import Diagram, PDPoint, QuotientSpace
from greedypermutation.clarksongreedy import greedy

class Sketch:
    def __init__(self, D: Diagram, n: int, seed=0):     #What should be the seed for a sketch?
        # self.diagram = D
        # self.numsketches = n

        sketches = greedy(M=D, seed=seed, nbrconstant=2, tree=True, gettransportplan=True)
        self._sketches = [next(sketches) for i in range(n)]
        # self._sketches = list(greedy(M=D, seed=seed, nbrconstant=2, tree=True, gettransportplan=True))

        self._state = {'index': 0, 'mass': self._sketches[0][2]}

    def __getitem__(self, index):
        # Different approach when slicing??
        if isinstance(index, slice):
            # return an generator which can iterate over the requested sketches
            indices = range(index.start, index.stop, index.step)
            return (self._sketches[i] for i in indices)
        else:
            # fetch self._sketches[index]
            sign = 1
            if index < self._state['index']:
                sign = -1
            while(index != self._state['index']):
                self._updateState(sign)
            return self._state['mass']

    def __iter__(self):
        return iter(self._sketches)

    def __hash__(self) -> int:
        return hash(tuple(self._sketches))

    def _updateState(self, sign):
        self._state['index'] += sign
        # sketch = self._sketches[self._state['index']]
        # transport = sketch[2]
        transport = self._sketches[self._state['index']][2]
        for p in transport:
            self._state['mass'][p] += sign*transport[p]
        
    def loadfromfile():
        pass

    def savetofile():
        pass