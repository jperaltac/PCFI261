#!/usr/bin/env python3

import matplotlib.pyplot as plt
from random import normalvariate
from math import sqrt

x, y = 0.0, 0.0

X = list()
Y = list()
for n in range(30000):
    x = x + normalvariate(0, sqrt(1.5))
    y = y + normalvariate(0, sqrt(1.5))
    X.append(x)
    Y.append(y)

plt.plot(X, Y)
plt.show()

