import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

rng = np.random.default_rng(42)

def oscillator(t, A, gamma, omega, phi):
    return A * np.exp(-gamma * t) * np.cos(omega * t + phi)

n_curves = 600
n_times = 80
t_grid = np.linspace(0.0, 8.0, n_times)

rows = []
for _ in range(n_curves):
    A = rng.uniform(0.5, 2.0)
    gamma = rng.uniform(0.03, 0.35)
    omega = rng.uniform(1.0, 4.0)
    phi = rng.uniform(0.0, np.pi)
    x = oscillator(t_grid, A, gamma, omega, phi)
    x += rng.normal(0.0, 0.015, size=n_times)

    for t, xt in zip(t_grid, x):
        rows.append([t, A, gamma, omega, phi, xt])

data = pd.DataFrame(rows, columns=["t", "A", "gamma", "omega", "phi", "x"])
X = data[["t", "A", "gamma", "omega", "phi"]].to_numpy()
y = data["x"].to_numpy()

X_train, X_tmp, y_train, y_tmp = train_test_split(
    X, y, test_size=0.30, random_state=42
)
X_val, X_test, y_val, y_test = train_test_split(
    X_tmp, y_tmp, test_size=0.50, random_state=42
)

scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_val_s = scaler.transform(X_val)
X_test_s = scaler.transform(X_test)

print(data.head())
print("train / val / test:", X_train_s.shape, X_val_s.shape, X_test_s.shape)
