#!/usr/bin/env python3

import matplotlib.pyplot as plt
from random import random

p = 0.6
delta = 0.5

def UpTo(n):
    x = 0.0
    for i in range(n):
        x = x + (delta*random() if random() < p else -delta*random())
    return x

X = [ UpTo(30) for i in range(1000000) ]

plt.hist(X, bins=70)
plt.show()
