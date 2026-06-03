def build_osc_regressor(width=256):
    net = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(5,)),
        tf.keras.layers.Dense(width, activation="relu"),
        tf.keras.layers.Dense(width, activation="relu"),
        tf.keras.layers.Dense(width, activation="relu"),
        tf.keras.layers.Dense(1),
    ])
    net.compile(optimizer="adam", loss="mse")
    return net

factor = 8
osc_X_big = np.tile(osc_X_train_s, (factor, 1))
osc_y_big = np.tile(osc_y_train, factor)

big_osc_model = build_osc_regressor(width=256)
t0 = time.perf_counter()
big_osc_model.fit(osc_X_big, osc_y_big, epochs=8, batch_size=1024, verbose=0)
osc_elapsed = time.perf_counter() - t0

print(f"Ejemplos usados: {len(osc_X_big):,}")
print(f"Tiempo entrenamiento: {osc_elapsed:.2f} s")
