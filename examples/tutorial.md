# A Tutorial for Using `pdsketch`

## Working with Diagrams

The `Diagram` class represents a persistence diagram, allowing points to have multiplicity.

```python {cmd id="import"}
from pdsketch import Diagram, SketchSequence
```

To begin, we can create a persistence diagram simply by adding some points.

```python {cmd continue="import"}
print(Diagram([(1,4), (4,14), (2,12)]))
```

Notice that in printing the diagram, we see each line has a `1` after the point.
This number is the multiplicity.
The default multiplicity of a point is `1`.
If we want to add points with multiplicity, we can pass a list of multiplicities along with the list of points as follows.

```python {cmd continue="import"}
print(Diagram([(1,4), (4,14), (2,12)], [10, 3, 2]))
```

Note that you have to specify a multiplicity for every point if you supply one for any point.
It is assumed that the list indices provides the correspondence between points and their masses.
If the lengths don't match, you will get an error like the following.

```python {cmd continue="import"}
Diagram([(1,4), (4,14), (2,12)], [10, 3])
```

Points can be manually added to a diagram after it has been initialized.
Yoiu may also add with multiplicity.

```python {cmd continue="import"}
D = Diagram()
D.add((1,2))
D.add((4,5), 6)
D.add((1,2), 3)
print(D)
```

## Working With Files

It is possible to read and write diagrams to files.

```python {cmd continue="import"}
D = Diagram([(1,4), (4,14), (2,12)], [10, 3, 2])
D.savetofile('D.dgm')

A = Diagram.loadfromfile('D.dgm')
print(A)
```


## Working with Sketches

The main reason for the existence of the `pdsketch` package is to efficiently sketch persistence diagrams.
A sketch is a summary that is smaller than the whole diagram, but meaningfully close.
In the case of persistence diagrams, proximity is measured by the bottleneck distance.

```python {cmd id=import}
from pdsketch import Diagram, SketchSequence
```

```python {cmd continue="import"}
D = Diagram([(i,j) for j in range(10) for i in range(j)])
S = SketchSequence(D)
```
