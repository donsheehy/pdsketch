from pdsketch import Sketch, PDPoint, Diagram
from random import randrange, seed

from pdsketch.plot_sketch import plot_sketch

M = 300
N = 100
n = 10
seed(0)

points = []
for i in range(N):
    x = randrange(5, M-5)
    points.append(PDPoint([x, randrange(x,M-5)]))

print(points)

D = Diagram(points)

S = Sketch(D, n)

# for i in range(2):
#     plot_sketch(S[i], filename="sketch_"+str(i))

S.savetofile()
S.loadfromfile("sketch")

for i in range(2):
    plot_sketch(S[i], filename="sketch_"+str(i))