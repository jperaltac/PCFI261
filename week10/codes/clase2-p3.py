transit_prob = transit_model.predict(tr_X_test_s, verbose=0).ravel()
transit_pred = (transit_prob >= 0.5).astype(int)

print(confusion_matrix(tr_y_test, transit_pred))
print(classification_report(tr_y_test, transit_pred, target_names=["sin tránsito", "con tránsito"]))

# Casos cercanos al umbral: son interesantes para discutir incertidumbre.
idx = np.argsort(np.abs(transit_prob - 0.5))[:4]
fig, axes = plt.subplots(2, 2, figsize=(8, 5), sharex=True, sharey=True)
for ax, j in zip(axes.ravel(), idx):
    ax.plot(transit_time_grid, tr_X_test[j], lw=1.5)
    ax.set_title(f"real={tr_y_test[j]}, p={transit_prob[j]:.2f}")
    ax.set_xlabel("tiempo relativo")
    ax.set_ylabel("flujo")
plt.tight_layout()
plt.show()
