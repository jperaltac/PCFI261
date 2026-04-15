#!/usr/bin/python3

import matplotlib.pyplot as plt
from math import sqrt, exp, pi
from numpy import linspace
from random import random

mu = 2.0
sigma = sqrt(1.5)
N = 1000000

def p(x): return exp(-0.5*(1.0/sigma**2)*(x-mu)**2)/(sqrt(2.0*pi)*sigma)

xmin, xmax = -10.0, 10.0
p_max = p(mu)

def rejection():
    while True:
        x = xmin + random()*(xmax-xmin)
        if random()*p_max < p(x): return x

data = [ rejection() for i in range(N) ]
X = linspace(min(data), max(data), 1000)

plt.hist(data, bins=70, normed=True)
plt.plot(X, [p(x) for x in X], 'r-', linewidth=2)
plt.show()
