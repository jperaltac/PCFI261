nonlinear_model = keras.Sequential([
    layers.Input(shape=(2,)),
    layers.Dense(16, activation="tanh"),
    layers.Dense(16, activation="tanh"),
    layers.Dense(1, activation="sigmoid")
])

nonlinear_model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.01),
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

nonlinear_model.summary()

history_nonlinear = nonlinear_model.fit(
    X_train_scaled, y_train,
    validation_data=(X_val_scaled, y_val),
    epochs=300,
    batch_size=32,
    verbose=0,
    callbacks=[early_stopping]
)

plot_history(history_nonlinear, title="Red neuronal no lineal")

test_loss_nl, test_acc_nl = nonlinear_model.evaluate(X_test_scaled, y_test, verbose=0)
print(f"Loss test (no lineal): {test_loss_nl:.4f}")
print(f"Accuracy test (no lineal): {test_acc_nl:.4f}")

plot_decision_boundary(nonlinear_model, X_test, y_test, title="Red no lineal sobre datos de prueba")
