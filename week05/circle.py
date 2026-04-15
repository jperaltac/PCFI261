#!/usr/bin/env python3

import matplotlib.pyplot as plt
from random import random

N = 10000
L = 1.0
R = 0.7

X = [ 2.0*random()*L-L for i in range(N) ]
Y = [ 2.0*random()*L-L for i in range(N) ]

Xc, Yc = list(), list()
for i in range(N):
    x, y = X[i], Y[i]
    if x**2+y**2 < R**2: 
       Xc.append(x)
       Yc.append(y)

print ((4.0*float(len(Xc))/float(len(X)))/(R*R))

plt.plot(X, Y, 'b.')
plt.plot(Xc, Yc, 'r.')
plt.show()
