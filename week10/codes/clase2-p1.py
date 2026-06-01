import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

rng = np.random.default_rng(123)

def make_light_curves(n_samples=6000, n_points=128, noise=0.003):
    time = np.linspace(-1.0, 1.0, n_points)
    curves = np.empty((n_samples, n_points), dtype="float32")
    labels = np.empty(n_samples, dtype="int32")

    for i in range(n_samples):
        has_transit = rng.random() < 0.5
        flux = 1.0 + rng.normal(0.0, noise, size=n_points)

        if has_transit:
            depth = rng.uniform(0.008, 0.030)
            width = rng.uniform(0.06, 0.16)
            center = rng.uniform(-0.25, 0.25)
            transit = np.abs(time - center) < width
            flux[transit] -= depth

        curves[i] = flux
        labels[i] = int(has_transit)

    return time, curves, labels

time_grid, curves, labels = make_light_curves()
X_train, X_tmp, y_train, y_tmp = train_test_split(
    curves, labels, test_size=0.30, stratify=labels, random_state=123
)
X_val, X_test, y_val, y_test = train_test_split(
    X_tmp, y_tmp, test_size=0.50, stratify=y_tmp, random_state=123
)

scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_val_s = scaler.transform(X_val)
X_test_s = scaler.transform(X_test)

print("Curvas:", curves.shape)
print("Fraccion con transito:", labels.mean().round(3))
