#!/usr/bin/env python3

import matplotlib.pyplot as plt
from random import randint, random
from statistics import mean, stdev
from numpy import linspace, arange
from math import exp, tanh

N, NSTEPS = 100, 50000
Y = list()

chain = [ (1 if random() < 0.5 else -1) for i in range(N) ]
def Energy(chain): return -sum(chain[i]*chain[i+1] for i in range(N-1))
def Ea(x): return -((N-1)/N)*tanh(1.0/x)

for T in arange(0.1, 4.1, 0.1):
    Eval = list()
    for n in range(NSTEPS):
        E1 = Energy(chain)
        k = randint(0, N-1)
        chain[k] = -chain[k]
        E2 = Energy(chain)
        E, chain[k] = ((E2, chain[k]) if random() < exp(-(1.0/T)*(E2-E1)) else (E1, -chain[k]))
        Eval.append(E/float(N-1))
    Y.append(mean(Eval))

plt.plot(arange(0.1, 4.1, 0.1), Y, 'b.')
plt.plot(linspace(0, 4.0, 1000), [ Ea(x) for x in linspace(0, 4.0, 1000)])
plt.xlabel('Temperatura')
plt.ylabel('Energía por spin')
plt.legend(['Monte Carlo', 'Solución analítica'], loc=2)
plt.show()
