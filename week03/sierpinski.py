#!/usr/bin/env python3

from math import tan, pi
from random import random
import matplotlib.pyplot as plt

L = 1.0

a = [ 0.0, L, 0.5*L ]
b = [ 0.0, 0.0, 0.5*L*tan(pi*60.0/180.0) ]

X = [ w for w in a ]
Y = [ w for w in b ]

x, y = 0.5*L, 0.25*L*tan(pi*60.0/180.0)
for i in range(1000):
    n = int(3*random())
    x = (x + a[n])/2.0
    y = (y + b[n])/2.0
    X.append(x)
    Y.append(y)

plt.scatter(X, Y, s=1)
plt.show()
