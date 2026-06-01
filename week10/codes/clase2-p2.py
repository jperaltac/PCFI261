import tensorflow as tf

tf.keras.utils.set_random_seed(123)

clf = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(X_train_s.shape[1],)),
    tf.keras.layers.Dense(64, activation="relu"),
    tf.keras.layers.Dense(32, activation="relu"),
    tf.keras.layers.Dense(1, activation="sigmoid"),
])

clf.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
    loss="binary_crossentropy",
    metrics=["accuracy", tf.keras.metrics.AUC(name="auc")],
)

history = clf.fit(
    X_train_s, y_train,
    validation_data=(X_val_s, y_val),
    epochs=25,
    batch_size=256,
    verbose=0,
)

print(dict(zip(clf.metrics_names, clf.evaluate(X_test_s, y_test, verbose=0))))
