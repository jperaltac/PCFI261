#!/usr/bin/env python3

from random import random
import matplotlib.pyplot as plt

X = list()
Y = list()

x, y = 0.5, 0.0 

def Evolve(x, y):
    xnew, ynew = None, None
    if random() < 0.02: xnew, ynew = (0.5, 0.27*y)
    elif random() <= 0.17: xnew, ynew = (-0.139*x+0.263*y+0.57, 0.246*x + 0.224*y-0.036)
    elif random() <= 0.3: xnew, ynew = (0.17*x-0.215*y+0.408, 0.222*x+0.176*y+0.0893)
    else: xnew, ynew = (0.781*x+0.034*y+0.1075, -0.032*x+0.739*y+0.27)
    return (xnew, ynew)

for i in range(150000):
    x, y = Evolve(x, y)
    X.append(x)
    Y.append(y)

plt.scatter(X, Y, s=1)
plt.show()
