#!/usr/bin/env python3

from math import *
import matplotlib.pyplot as plt
from numpy import linspace

def f(t): return exp(-t/2.0)*cos(15.0*t)

X = linspace(2.0, 5.0, 1000)
Y = [ f(x) for x in X ]

plt.plot(X, Y, 'b-')
plt.xlabel("$t$")
plt.ylabel("$f(t)$")
plt.show()

