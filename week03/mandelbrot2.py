#!/usr/bin/env python3

import numpy as np
import pylab as plt

def Iterate(x, y):
    z0, zp = complex(x, y), complex(0, 0)
    for k in range(500):
        zp = zp**2 + z0
        if abs(zp) > 2: return k+1
    return 0

N = 5000

t1 = np.linspace(-1.5, 1.5, N)
t2 = np.linspace(-1.5, 1.5, N)

mset = np.zeros((N, N))

for i, x in enumerate(t1):
    for j, y in enumerate(t2):
        mset[i, j] = Iterate(x, y)

plt.imshow(mset, cmap='jet')
plt.show()
