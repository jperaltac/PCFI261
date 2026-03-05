#!/usr/bin/env python3

import matplotlib.pyplot as plt
from math import acos, pi

def logistic(mu, x): return mu*float(x)*(1.0-float(x))

mu = 3.999
seed = 0.75
N = 50000

x = seed
X = list()
for i in range(N):
    X.append(x)
    x = logistic(mu, x)

Y = [(1.0/pi)*acos(1.0-2.0*x) for x in X]

f, arr = plt.subplots(2,  sharex=True)
arr[0].hist(X)
arr[1].hist(Y)
plt.show()

