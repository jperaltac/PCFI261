dense_model = keras.Sequential([
    layers.Input(shape=(28, 28)),
    layers.Flatten(),
    layers.Dense(128, activation="relu"),
    layers.Dropout(0.20),
    layers.Dense(10, activation="softmax"),
])

dense_model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"],
)

dense_history = dense_model.fit(
    x_train, y_train,
    validation_data=(x_val, y_val),
    epochs=6,
    batch_size=128,
)

dense_model.summary()
