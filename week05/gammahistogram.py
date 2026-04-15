#!/usr/bin/python3

import matplotlib.pyplot as plt
from random import gammavariate
from mpmath import gamma, exp
from numpy import linspace

k = 7.5
theta = 3.0
N = 1000000

def p(x): return (exp(-x/theta)*(x**(k-1)))/(gamma(k)*(theta**k))

data = [ gammavariate(k, theta) for i in range(N) ]
X = linspace(0, max(data), 1000)

plt.hist(data, bins=70, normed=True)
plt.plot(X, [p(x) for x in X], 'r-', linewidth=2)
plt.show()
