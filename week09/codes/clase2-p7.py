RUN_HEAVY_EXPERIMENT = False

if RUN_HEAVY_EXPERIMENT:
    n_samples = 60000
    n_features = 512
    rng = np.random.default_rng(261)
    X_big = rng.normal(size=(n_samples, n_features)).astype("float32")
    w = rng.normal(size=(n_features, 1)).astype("float32")
    logits = X_big @ w + 0.25 * rng.normal(size=(n_samples, 1)).astype("float32")
    y_big = (logits.ravel() > np.median(logits)).astype("float32")

    Xb_train, Xb_test, yb_train, yb_test = train_test_split(
        X_big,
        y_big,
        test_size=0.20,
        random_state=261,
        stratify=y_big,
    )

    tf.keras.backend.clear_session()
    big_model = keras.Sequential(
        [
            layers.Input(shape=(n_features,)),
            layers.Dense(4096, activation="relu"),
            layers.Dense(4096, activation="relu"),
            layers.Dense(2048, activation="relu"),
            layers.Dense(1, activation="sigmoid"),
        ]
    )

    big_model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=1e-3),
        loss="binary_crossentropy",
        metrics=["accuracy"],
    )

    big_model.summary()
    big_model.fit(
        Xb_train,
        yb_train,
        validation_split=0.20,
        epochs=5,
        batch_size=512,
        verbose=1,
    )
    big_model.evaluate(Xb_test, yb_test, verbose=1)
