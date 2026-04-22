#!/usr/bin/env python3

#
# Estas funciones manejan la ventana grafica, 
# las animaciones y las condiciones periodicas
# El usuario final no necesita modificar nada de esto
#
import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.cm as cm

from numpy import zeros

A, im, cols, rws, pbc = None, None, -1, -1, False

def SetMatrixSize(columns, rows, periodic=False):
    global cols, rws, pbc
    cols, rws, pbc = columns, rows, periodic

def GetMatrixValue(column, row):
    if column < 0: column = (column+cols if pbc else None)
    if column > cols-1: column = (column-cols if pbc else None)
    if row < 0: row = (row+rws if pbc else None)
    if row > rws-1: row = (row-rws if pbc else None)
    return A[row][column]

def SetMatrixValues(A, rws, cols, func):
    for i in range(rws):
        for j in range(cols): A[i][j] = func(i, j)

def updatefig(*args):
    global A
    SetMatrixValues(A, rws, cols, UpdateMatrix)
    im.set_array(A)
    return im,

def Show(interval=None):
    global A, im
    A, fig = zeros((rws, cols)), plt.figure()
    SetMatrixValues(A, rws, cols, InitializeMatrix)
    im = plt.imshow(A, interpolation='nearest', cmap=cm.coolwarm)
    if interval is not None: ani = animation.FuncAnimation(fig, updatefig, interval=interval, blit=True)
    plt.show()

#
# De aqui en adelante sigue el codigo modificable por el usuario...
#
# Este ejemplo es una implementacion de Monte Carlo Metropolis para el modelo de Ising
#
from random import random
from math import exp

T = float(sys.argv[1])
beta = 1.0/T

SetMatrixSize(columns=100, rows=100, periodic=True)

def InitializeMatrix(row, column): return (1.0 if random() < 0.5 else 0.0)

def dEnergy(row, column):
    S = sum(2.0*GetMatrixValue(column+dc, row+dr)-1.0 for (dc, dr) in ((1, 0), (-1, 0), (0, -1), (0, 1)))
    return (2.0*GetMatrixValue(column, row)-1.0)*S

def UpdateMatrix(row, column):
    old = GetMatrixValue(column, row)
    if random() < 0.5: return old
    flipped = (1.0 if old < 0.5 else 0.0)
    return (flipped if random() < exp(-beta*dEnergy(row, column)) else old)

Show(interval=1)

