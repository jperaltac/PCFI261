#!/usr/bin/env python3

import random

N = 10000
V = 1.0  # largo del intervalo [0,1]

samples = [random.random() for _ in range(N)]  # puntos uniformes en [0,1]
values = [x**2 for x in samples]

Q_N = V * sum(values) / N

print(f"Estimacion Monte Carlo: {Q_N:.6f}")
print(f"Valor exacto: {1/3:.6f}")
