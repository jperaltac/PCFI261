tf.keras.utils.set_random_seed(42)

osc_model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(5,)),
    tf.keras.layers.Dense(64, activation="relu"),
    tf.keras.layers.Dense(64, activation="relu"),
    tf.keras.layers.Dense(1),
])

osc_model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
    loss="mse",
    metrics=[tf.keras.metrics.RootMeanSquaredError(name="rmse")],
)

osc_history = osc_model.fit(
    osc_X_train_s, osc_y_train,
    validation_data=(osc_X_val_s, osc_y_val),
    epochs=40,
    batch_size=256,
    verbose=0,
)

osc_test_loss, osc_test_rmse = osc_model.evaluate(osc_X_test_s, osc_y_test, verbose=0)
print(f"MSE test:  {osc_test_loss:.5f}")
print(f"RMSE test: {osc_test_rmse:.5f}")
