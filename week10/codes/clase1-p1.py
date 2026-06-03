# Requiere haber ejecutado la celda de preparación del notebook.
osc_rng = np.random.default_rng(42)

def oscillator(t, A, gamma, omega, phi):
    return A * np.exp(-gamma * t) * np.cos(omega * t + phi)

n_curves = 600
n_times = 80
osc_t_grid = np.linspace(0.0, 8.0, n_times)

rows = []
for _ in range(n_curves):
    A = osc_rng.uniform(0.5, 2.0)
    gamma = osc_rng.uniform(0.03, 0.35)
    omega = osc_rng.uniform(1.0, 4.0)
    phi = osc_rng.uniform(0.0, np.pi)
    x = oscillator(osc_t_grid, A, gamma, omega, phi)
    x += osc_rng.normal(0.0, 0.015, size=n_times)

    for t, xt in zip(osc_t_grid, x):
        rows.append([t, A, gamma, omega, phi, xt])

osc_data = pd.DataFrame(rows, columns=["t", "A", "gamma", "omega", "phi", "x"])
osc_X = osc_data[["t", "A", "gamma", "omega", "phi"]].to_numpy()
osc_y = osc_data["x"].to_numpy()

osc_X_train, osc_X_tmp, osc_y_train, osc_y_tmp = train_test_split(
    osc_X, osc_y, test_size=0.30, random_state=42
)
osc_X_val, osc_X_test, osc_y_val, osc_y_test = train_test_split(
    osc_X_tmp, osc_y_tmp, test_size=0.50, random_state=42
)

osc_scaler = StandardScaler()
osc_X_train_s = osc_scaler.fit_transform(osc_X_train)
osc_X_val_s = osc_scaler.transform(osc_X_val)
osc_X_test_s = osc_scaler.transform(osc_X_test)

osc_data.head()
