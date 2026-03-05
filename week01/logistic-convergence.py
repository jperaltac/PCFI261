#!/usr/bin/env python3

import matplotlib.pyplot as plt

def logistic(mu, x): return mu*x*(1-x)

mu = 3.5
seed = 0.75
N = 40

x = seed
X = list()
for i in range(N):
    X.append(x)
    x = logistic(mu, x)

plt.plot(range(N), X)
plt.xlabel("$n$")
plt.ylabel("$x_n$")
plt.show()

