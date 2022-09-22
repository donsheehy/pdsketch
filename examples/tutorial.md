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
Diagram([(1,4), (4,14), (2,12)], [10, 3, 5])
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
D.save_to_file('D.dgm')

A = Diagram.load_from_file('D.dgm')
print(A)
```


## Working with Sketches

The main reason for the existence of the `pdsketch` package is to efficiently sketch persistence diagrams.
A sketch is a summary that is smaller than the whole diagram, but meaningfully close.
In the case of persistence diagrams, proximity is measured by the bottleneck distance.
We first import the `Diagram` and `SketchSequence` classes as follows.

```python {cmd id=import}
from pdsketch import Diagram, SketchSequence
```

Now, we will make a very simple diagram and sketch it.

```python {cmd continue="import" id="firstsketch"}
D = Diagram([(i,j) for j in range(7) for i in range(j)])
S = SketchSequence(D)
```

```python {cmd continue}
print(S)
```

The `SketchSequence` object gives us access to sketches of the diagram for any number of points.
The individual sketches are `Diagram`s.
They can be accessed by indexing into the sketch.
Here is an example of a sketch with three points (plus the diagonal).

```python {cmd continue="firstsketch"}
print(S[3])
```

A sketch with ten points (plus the diagonal).


```python {cmd continue="firstsketch"}
print(S[10])
```

Note that the individual sketches are not entirely precomputed, because that would require quadratic space.
Instead, they are stored in a form so that the $k$th diagram can be extracted in $O(k)$ time.

You can sketch a diagram that already has multiplicity.

```python {cmd continue="import"}
D = Diagram([(2,5), (6,13), (9,11)], [5,6,7])
S = SketchSequence(D)

print('----------\none point\n----------')
print(S[1])
print('----------\ntwo points\n----------')
print(S[2])
print('----------\nthree points\n----------')
print(S[3])
```

Notice that the last sketch doesn't include the diagonal.
That is because none of the extra mass is stored on the diagonal.



## Saving and Loading Sketches

A `SketchSequence` is stored as a special ordering on the points of a diagram with some extra information needed to construct the individual sketches.
That extra information is in the form of a transportation plan.
For the $i$th point, it tells how much mass to move from the other points to the $i$th point.
This is stored internally as a dictionary because there are only a constant number of points involved in the transportation plan for each point.


```python {cmd continue="import"}
D = Diagram([(i,j) for j in range(10) for i in range(j)])
S = SketchSequence(D)

S.save_to_file('sketch.dgm')

X = SketchSequence.load_from_file('sketch.dgm')
print(X[3])
```

A sketch sequence file is also a valid diagram file.
This is important.
It means that you can save a sketch and still use it as a diagram.

```python {cmd continue="import"}
D = Diagram([(i,+ 10) for i in range(6)])
S = SketchSequence(D)
S.save_to_file('sketch.dgm')

X = Diagram.load_from_file('sketch.dgm')
print(f'original D:\n{D}\n----')
print(f'sketch X:\n{X}\n----')
```

Notice that the order is changed.
The new order corresponds to the sketch order.
