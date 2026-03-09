#!/usr/bin/env python3

import matplotlib.pyplot as plt

a = 0.5471
b = 0.0281
c = 0.0266
m = 0.8439

h = 0.0001

def f(x, y): return a*x - b*x*y
def g(x, y): return c*x*y - m*y

t = 0
x, y = 30.0, 4.0

T = list()
X, Y = list(), list()
while t < 100.0:
    k1 = f(x, y)
    k2 = f(x+(h/2.0)*k1, y)
    k3 = f(x+(h/2.0)*k2, y)
    k4 = f(x+h*k3, y)
    xnew = x + (h/6.0)*(k1+2*k2+2*k3+k4)
    #xnew = x + h*k1
    #
    k1 = g(x, y)
    k2 = g(x, y+(h/2.0)*k1)
    k3 = g(x, y+(h/2.0)*k2)
    k4 = g(x, y+h*k3)
    ynew = y + (h/6.0)*(k1+2*k2+2*k3+k4)
    #ynew = y + h*k1
    x, y = xnew, ynew
    t = t + h
    X.append(x)
    Y.append(y)
    T.append(t)

#plt.plot(T, X, label='conejos')
#plt.plot(T, Y, label='zorros')
#plt.legend()
plt.plot(X, Y)
plt.show()
