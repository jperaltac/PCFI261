tf.keras.utils.set_random_seed(123)

transit_model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(tr_X_train_s.shape[1],)),
    tf.keras.layers.Dense(64, activation="relu"),
    tf.keras.layers.Dense(32, activation="relu"),
    tf.keras.layers.Dense(1, activation="sigmoid"),
])

transit_model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
    loss="binary_crossentropy",
    metrics=["accuracy", tf.keras.metrics.AUC(name="auc")],
)

transit_history = transit_model.fit(
    tr_X_train_s, tr_y_train,
    validation_data=(tr_X_val_s, tr_y_val),
    epochs=25,
    batch_size=256,
    verbose=0,
)

results = transit_model.evaluate(tr_X_test_s, tr_y_test, verbose=0)
print(dict(zip(transit_model.metrics_names, results)))
