from pdsketch import Sketch, PDPoint, Diagram
from random import randrange, seed

M = 3000
N = 50
n = 10
seed(0)

points = []
for i in range(N):
    x = randrange(5, M-5)
    points.append(PDPoint([x, randrange(x,M-5)]))

print(points)

D = Diagram(points)

S = Sketch(D, n)

for i in range(n):
    print(S[i])