def plot_history(history, title="Historia de entrenamiento"):
    hist = history.history
    epochs = range(1, len(hist["loss"]) + 1)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    axes[0].plot(epochs, hist["loss"], label="train loss")
    axes[0].plot(epochs, hist["val_loss"], label="val loss")
    axes[0].set_xlabel("Epoch")
    axes[0].set_ylabel("Loss")
    axes[0].set_title(title + " - pérdida")
    axes[0].legend()

    axes[1].plot(epochs, hist["accuracy"], label="train acc")
    axes[1].plot(epochs, hist["val_accuracy"], label="val acc")
    axes[1].set_xlabel("Epoch")
    axes[1].set_ylabel("Accuracy")
    axes[1].set_title(title + " - accuracy")
    axes[1].legend()

    plt.tight_layout()
    plt.show()


def plot_decision_boundary(model, X_plot, y_plot, title="Frontera de decisión"):
    x_min, x_max = X_plot[:, 0].min() - 0.8, X_plot[:, 0].max() + 0.8
    y_min, y_max = X_plot[:, 1].min() - 0.8, X_plot[:, 1].max() + 0.8
    xx, yy = np.meshgrid(
        np.linspace(x_min, x_max, 300),
        np.linspace(y_min, y_max, 300)
    )

    grid = np.c_[xx.ravel(), yy.ravel()]
    grid_scaled = scaler.transform(grid)
    probs = model.predict(grid_scaled, verbose=0).reshape(xx.shape)

    plt.figure(figsize=(6, 5))
    plt.contourf(xx, yy, probs, levels=30, cmap="coolwarm", alpha=0.55)
    plt.contour(xx, yy, probs, levels=[0.5], colors="black", linewidths=2)
    plt.scatter(X_plot[:, 0], X_plot[:, 1], c=y_plot, cmap="coolwarm", s=18, edgecolor="k")
    plt.xlabel("x1")
    plt.ylabel("x2")
    plt.title(title)
    plt.show()
