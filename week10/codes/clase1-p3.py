import matplotlib.pyplot as plt

case = {"A": 1.35, "gamma": 0.12, "omega": 2.7, "phi": 0.4}
t_plot = np.linspace(0.0, 8.0, 250)

X_curve = np.column_stack([
    t_plot,
    np.full_like(t_plot, case["A"]),
    np.full_like(t_plot, case["gamma"]),
    np.full_like(t_plot, case["omega"]),
    np.full_like(t_plot, case["phi"]),
])

y_true = oscillator(t_plot, **case)
y_pred = model.predict(scaler.transform(X_curve), verbose=0).ravel()
rmse_curve = np.sqrt(np.mean((y_true - y_pred) ** 2))

plt.figure(figsize=(7, 3.5))
plt.plot(t_plot, y_true, label="modelo fisico", lw=2)
plt.plot(t_plot, y_pred, "--", label="red densa", lw=2)
plt.xlabel("t")
plt.ylabel("x(t)")
plt.title(f"Curva no vista: RMSE={rmse_curve:.4f}")
plt.legend()
plt.tight_layout()
plt.show()
