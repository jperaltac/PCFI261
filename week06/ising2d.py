#!/usr/bin/env python3

import matplotlib.pyplot as plt
from random import randint, random
from statistics import mean, stdev
from numpy import linspace, arange
from math import exp

J = 1.0
N, NSTEPS = 32, 200000
Y = list()

mat = [ [ (1 if random() < 0.5 else -1) for i in range(N) ] for j in range(N) ]

def M(i, j):
    if i < 0: i += N
    if i > N-1: i -= N
    if j < 0: j += N
    if j > N-1: j -= N
    return mat[i][j]

def Energy(mat):
    S = 0.0
    for i in range(N):
        for j in range(N):
            S += mat[i][j]*(M(i+1, j)+M(i, j+1))
    return -J*S

def Magnetiz(mat):
    S = 0.0
    for i in range(N):
        for j in range(N):
            S += mat[i][j]
    return S

for T in linspace(0.1, 4.1, 30):
    Eval = list()
    print (T)
    for n in range(NSTEPS):
        E1 = Energy(mat)
        k1, k2 = randint(0, N-1), randint(0, N-1)
        mat[k1][k2] = -mat[k1][k2]
        E2 = Energy(mat)
        E, mat[k1][k2] = ((E2, mat[k1][k2]) if random() < exp(-(1.0/T)*(E2-E1)) else (E1, -mat[k1][k2]))
        magnet = abs(Magnetiz(mat))
        Eval.append(magnet/float(N*N))
        #Eval.append(E/float(N*N))
    Y.append(mean(Eval))

plt.plot(arange(0.1, 4.1, 0.1), Y, 'b.')
plt.xlabel('Temperatura')
#plt.ylabel('Energía por spin')
plt.ylabel('Magnetizacion')
plt.show()
