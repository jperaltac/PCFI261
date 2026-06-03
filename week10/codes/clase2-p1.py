transit_rng = np.random.default_rng(123)

def make_light_curves(n_samples=6000, n_points=128, noise=0.003):
    time_grid = np.linspace(-1.0, 1.0, n_points)
    curves = np.empty((n_samples, n_points), dtype="float32")
    labels = np.empty(n_samples, dtype="int32")

    for i in range(n_samples):
        has_transit = transit_rng.random() < 0.5
        flux = 1.0 + transit_rng.normal(0.0, noise, size=n_points)

        if has_transit:
            depth = transit_rng.uniform(0.008, 0.030)
            width = transit_rng.uniform(0.06, 0.16)
            center = transit_rng.uniform(-0.25, 0.25)
            in_transit = np.abs(time_grid - center) < width
            flux[in_transit] -= depth

        curves[i] = flux
        labels[i] = int(has_transit)

    return time_grid, curves, labels

transit_time_grid, transit_curves, transit_labels = make_light_curves()

tr_X_train, tr_X_tmp, tr_y_train, tr_y_tmp = train_test_split(
    transit_curves, transit_labels, test_size=0.30, stratify=transit_labels, random_state=123
)
tr_X_val, tr_X_test, tr_y_val, tr_y_test = train_test_split(
    tr_X_tmp, tr_y_tmp, test_size=0.50, stratify=tr_y_tmp, random_state=123
)

transit_scaler = StandardScaler()
tr_X_train_s = transit_scaler.fit_transform(tr_X_train)
tr_X_val_s = transit_scaler.transform(tr_X_val)
tr_X_test_s = transit_scaler.transform(tr_X_test)

print("Curvas:", transit_curves.shape)
print("Fracción con tránsito:", transit_labels.mean().round(3))
