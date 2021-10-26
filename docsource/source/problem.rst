===========
The Problem
===========


.. What is the problem you are trying to solve?

A *persistence diagram* is a set, each element of which has a pair of numbers called the birth and death.
The death is permitted to be infinity and multiple points of the persistence diagram may have the same birth and death times.
The elements of a persistence diagram are called **points**, though if one identifies the points with their birth-death times, the diagram may be a multiset.

The **pdsketch** library is an implementation of the algorithms in the paper, Sketching Persistence Diagrams by Donald R. Sheehy and Siddharth Sheth.
The goal is to provide progressively more precise sketches of a persistence diagram by representing it as set with multiplicity.
For any given integer k, one can have a persistence diagram with k points.
The algorithm approximates the closest k-point diagram to the input diagram (in bottleneck distance).
