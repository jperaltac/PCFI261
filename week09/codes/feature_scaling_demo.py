import numpy as np

rng = np.random.default_rng(261)

# Dos variables con escalas muy distintas.
depth = rng.normal(loc=0.015, scale=0.004, size=8)
snr = rng.normal(loc=35.0, scale=12.0, size=8)

X = np.column_stack([depth, snr])

mu = X.mean(axis=0)
sigma = X.std(axis=0)
X_scaled = (X - mu) / sigma

print("media original:", mu)
print("desviacion original:", sigma)
print("primeras filas escaladas:")
print(np.round(X_scaled[:4], 3))
