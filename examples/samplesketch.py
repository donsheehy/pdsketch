from pdsketch import Sketch, PDPoint, Diagram, Diagram2
from random import randrange, seed

M = 30
N = 50
n = 10
seed(0)

points = []
for i in range(N):
    x = randrange(5, M-5)
    points.append(PDPoint([x, randrange(x,M-5)]))

D = Diagram2(points)

S = Sketch(D, n)

print("Sketching is fun")
for i in range(n):
    print(S[i])