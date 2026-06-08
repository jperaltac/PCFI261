augment = keras.Sequential([
    layers.RandomRotation(0.08),
    layers.RandomTranslation(0.08, 0.08),
    layers.RandomZoom(0.08),
])

cnn_aug = keras.Sequential([
    layers.Input(shape=(28, 28, 1)),
    augment,
    layers.Conv2D(8, 3, activation="relu", padding="same"),
    layers.MaxPooling2D(2),
    layers.Conv2D(16, 3, activation="relu", padding="same"),
    layers.MaxPooling2D(2),
    layers.Flatten(),
    layers.Dense(64, activation="relu"),
    layers.Dense(10, activation="softmax"),
])

cnn_aug.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"],
)

history_aug = cnn_aug.fit(
    x_train_cnn, y_train,
    validation_data=(x_val_cnn, y_val),
    epochs=4,
    batch_size=128,
)
