def plot_history(history, title):
    hist = pd.DataFrame(history.history)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    axes[0].plot(hist["loss"], label="train")
    axes[0].plot(hist["val_loss"], label="validation")
    axes[0].set_title(f"{title}: loss")
    axes[0].set_xlabel("epoch")
    axes[0].legend()
    axes[1].plot(hist["accuracy"], label="train")
    axes[1].plot(hist["val_accuracy"], label="validation")
    axes[1].set_title(f"{title}: accuracy")
    axes[1].set_xlabel("epoch")
    axes[1].legend()
    plt.tight_layout()
    plt.show()

experiments = [
    {"name": "muy pequena", "hidden_layers": (4,), "learning_rate": 1e-3, "dropout": 0.0},
    {"name": "base", "hidden_layers": (16, 8), "learning_rate": 1e-3, "dropout": 0.0},
    {"name": "mas neuronas", "hidden_layers": (64, 32), "learning_rate": 1e-3, "dropout": 0.0},
    {"name": "regularizada", "hidden_layers": (64, 32), "learning_rate": 1e-3, "dropout": 0.25},
]

results = []
trained_models = {}

for cfg in experiments:
    tf.keras.backend.clear_session()
    tf.random.set_seed(261)
    exp_model = build_mlp(
        hidden_layers=cfg["hidden_layers"],
        learning_rate=cfg["learning_rate"],
        dropout=cfg["dropout"],
    )
    exp_history = exp_model.fit(
        X_train_s,
        y_train,
        validation_data=(X_val_s, y_val),
        epochs=200,
        batch_size=32,
        callbacks=[early_stop],
        verbose=0,
    )
    val_loss, val_acc, val_auc = exp_model.evaluate(X_val_s, y_val, verbose=0)
    trained_models[cfg["name"]] = exp_model
    results.append(
        {
            "modelo": cfg["name"],
            "capas": cfg["hidden_layers"],
            "dropout": cfg["dropout"],
            "parametros": exp_model.count_params(),
            "epochs": len(exp_history.history["loss"]),
            "val_loss": val_loss,
            "val_accuracy": val_acc,
            "val_auc": val_auc,
        }
    )

pd.DataFrame(results).sort_values("val_auc", ascending=False)
