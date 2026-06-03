# Evaluamos una curva completa no usada explícitamente para entrenar.
case = {"A": 1.35, "gamma": 0.12, "omega": 2.7, "phi": 0.4}
osc_t_plot = np.linspace(0.0, 8.0, 250)

osc_X_curve = np.column_stack([
    osc_t_plot,
    np.full_like(osc_t_plot, case["A"]),
    np.full_like(osc_t_plot, case["gamma"]),
    np.full_like(osc_t_plot, case["omega"]),
    np.full_like(osc_t_plot, case["phi"]),
])

osc_y_true = oscillator(osc_t_plot, **case)
osc_y_pred = osc_model.predict(osc_scaler.transform(osc_X_curve), verbose=0).ravel()
osc_rmse_curve = np.sqrt(np.mean((osc_y_true - osc_y_pred) ** 2))

plt.figure(figsize=(8, 4))
plt.plot(osc_t_plot, osc_y_true, label="modelo físico", lw=2)
plt.plot(osc_t_plot, osc_y_pred, "--", label="red densa", lw=2)
plt.xlabel("t")
plt.ylabel("x(t)")
plt.title(f"Curva no vista: RMSE={osc_rmse_curve:.4f}")
plt.legend()
plt.show()
