#!/usr/bin/env python3

import matplotlib.pyplot as plt
from random import random

p = 0.51
delta = 0.1
x = 0.0

X = list()
for n in range(100000):
    x = x + (delta if random() < p else -delta)
    X.append(x)

plt.plot(range(len(X)), X)
plt.xlabel('Tiempo')
plt.ylabel('Posición')
plt.show()

