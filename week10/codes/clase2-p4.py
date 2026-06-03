def build_large_transit_classifier(n_points):
    net = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(n_points,)),
        tf.keras.layers.Dense(512, activation="relu"),
        tf.keras.layers.Dense(256, activation="relu"),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dense(1, activation="sigmoid"),
    ])
    net.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
    return net

_, tr_X_big_raw, tr_y_big = make_light_curves(n_samples=40000, n_points=128, noise=0.004)
tr_X_big = transit_scaler.transform(tr_X_big_raw)

big_transit_model = build_large_transit_classifier(tr_X_big.shape[1])
t0 = time.perf_counter()
big_transit_model.fit(tr_X_big, tr_y_big, epochs=6, batch_size=1024, validation_split=0.2, verbose=0)
transit_elapsed = time.perf_counter() - t0

print(f"Ejemplos usados: {len(tr_X_big):,}")
print(f"Tiempo entrenamiento: {transit_elapsed:.2f} s")
