test_loss, test_acc = dense_model.evaluate(x_test, y_test, verbose=0)
print(f"accuracy test red densa: {test_acc:.4f}")

y_prob_dense = dense_model.predict(x_test, verbose=0)
y_pred_dense = np.argmax(y_prob_dense, axis=1)

errores = np.where(y_pred_dense != y_test)[0]
print("primeros errores:", errores[:10])

fig, axes = plt.subplots(2, 5, figsize=(8, 3.4))
for ax, idx in zip(axes.ravel(), errores[:10]):
    ax.imshow(x_test[idx], cmap="gray_r")
    ax.set_title(f"real {y_test[idx]} / pred {y_pred_dense[idx]}")
    ax.axis("off")
plt.tight_layout()
