#!/usr/bin/env python3

import numpy as np
import pylab as plt
from random import randint

N = 1000

t1 = np.linspace(-1, 1, N)
t2 = np.linspace(-1, 1, N)
mset = np.zeros((N, N))

for i, x in enumerate(t1):
    for j, y in enumerate(t2):
        mset[i, j] = randint(1, 50)

plt.imshow(mset, cmap='jet')
plt.show()
