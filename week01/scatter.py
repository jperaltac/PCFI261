#!/usr/bin/env python3

from math import *
import matplotlib.pyplot as plt
from random import random

N = 100000
R = 3.0

def signrandom(): return 2.0*random()-1.0

X = [signrandom()*10.0 for i in range(N)]
Y = [signrandom()*10.0 for i in range(N)]

Xs, Ys = list(), list()
for i in range(N):
    if sqrt(X[i]*X[i]+Y[i]*Y[i]) < R:
       Xs.append(X[i])
       Ys.append(Y[i])

plt.scatter(Xs, Ys, s=1)
plt.xlabel("$x$")
plt.ylabel("$y$")
plt.show()

