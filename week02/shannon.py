#!/usr/bin/env python3

import matplotlib.pyplot as plt
from random import normalvariate, gammavariate
from math import *

def Entropy(data, a, b, N):
    p = [0 for i in range(N)]
    for x in data:
        i = int(((x-a)/(b-a))*N)
        p[i] = p[i] + 1
    S = sum(p)
    for i in range(N): p[i] = p[i]/S
    return sum(( 0 if pi == 0 else -pi*log(pi)) for pi in p)

data = [gammavariate(0.8, 1.5) for i in range(1000)]
print (Entropy(data, -10.0, 10.0, 70))

plt.hist(data, bins=70)
plt.show()

