def build_mlp(hidden_layers=(16, 8), learning_rate=1e-3, dropout=0.0):
    model = keras.Sequential()
    model.add(layers.Input(shape=(X_train_s.shape[1],)))

    for neurons in hidden_layers:
        model.add(layers.Dense(neurons, activation="relu"))
        if dropout > 0:
            model.add(layers.Dropout(dropout))

    model.add(layers.Dense(1, activation="sigmoid"))

    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
        loss="binary_crossentropy",
        metrics=["accuracy", keras.metrics.AUC(name="auc")],
    )
    return model

model = build_mlp(hidden_layers=(16, 8), learning_rate=1e-3, dropout=0.0)
model.summary()

early_stop = keras.callbacks.EarlyStopping(
    monitor="val_loss",
    patience=20,
    restore_best_weights=True,
)

history = model.fit(
    X_train_s,
    y_train,
    validation_data=(X_val_s, y_val),
    epochs=200,
    batch_size=32,
    callbacks=[early_stop],
    verbose=0,
)

pd.DataFrame(history.history).tail()
