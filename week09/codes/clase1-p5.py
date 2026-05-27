linear_model = keras.Sequential([
    layers.Input(shape=(2,)),
    layers.Dense(1, activation="sigmoid")
])

linear_model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.01),
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

linear_model.summary()

plot_keras_architecture(
    linear_model,
    input_dim=2,
    title="Arquitectura del modelo lineal",
    max_neurons=12
)

early_stopping = keras.callbacks.EarlyStopping(
    monitor="val_loss",
    patience=20,
    restore_best_weights=True
)

history_linear = linear_model.fit(
    X_train_scaled, y_train,
    validation_data=(X_val_scaled, y_val),
    epochs=200,
    batch_size=32,
    verbose=0,
    callbacks=[early_stopping]
)

plot_history(history_linear, title="Modelo lineal")

plot_keras_weight_heatmaps(
    linear_model,
    title="Pesos aprendidos por el modelo lineal"
)

test_loss_linear, test_acc_linear = linear_model.evaluate(X_test_scaled, y_test, verbose=0)
print(f"Loss test (lineal): {test_loss_linear:.4f}")
print(f"Accuracy test (lineal): {test_acc_linear:.4f}")

plot_decision_boundary(linear_model, X_test, y_test, title="Modelo lineal sobre datos de prueba")
