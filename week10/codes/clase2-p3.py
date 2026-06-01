from sklearn.metrics import confusion_matrix, classification_report
import matplotlib.pyplot as plt

prob = clf.predict(X_test_s, verbose=0).ravel()
y_pred = (prob >= 0.5).astype(int)

print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred, target_names=["sin transito", "con transito"]))

idx = np.argsort(np.abs(prob - 0.5))[:4]
fig, axes = plt.subplots(2, 2, figsize=(8, 5), sharex=True, sharey=True)
for ax, j in zip(axes.ravel(), idx):
    ax.plot(time_grid, X_test[j], lw=1.5)
    ax.set_title(f"real={y_test[j]}, p={prob[j]:.2f}")
    ax.set_xlabel("tiempo relativo")
    ax.set_ylabel("flujo")
plt.tight_layout()
plt.show()
