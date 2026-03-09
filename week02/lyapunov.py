#!/usr/bin/env python3

import matplotlib.pyplot as plt
from math import *
from random import random
from numpy import linspace

def logistic(mu, x): return mu*x*(1-x)

mu = 3.99

def Lyapunov(mu):
    N = 500
    x = random()
    S = 0.0
    for i in range(N):
        S += log(abs(mu*(1.0-2.0*x)))
        x = logistic(mu, x)
    return S/N

MU = linspace(2.5, 3.999, 1000)
plt.plot(MU, [Lyapunov(mu) for mu in MU])
plt.xlabel("$\mu$")
plt.ylabel("$\lambda(\mu)$")
plt.show()

