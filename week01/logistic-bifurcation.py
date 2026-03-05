#!/usr/bin/env python3

import matplotlib.pyplot as plt
from numpy import linspace
from random import choice, random

def logistic(mu, x): return mu*x*(1-x)

def converged(mu):
    seed = random()
    x = seed
    for n in range(1000): x = logistic(mu, x)
    return x

mu_values = linspace(1.0, 4.0, 10000)
MU = [choice(mu_values) for i in range(50000)]
xstar = [converged(mu) for mu in MU]

plt.scatter(MU, xstar, s=2)
plt.xlim(1.0, 4.0)
plt.xlabel("$\mu$")
plt.ylabel("$x^*$")
plt.show()

