import time

def build_large_classifier(n_points):
    net = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(n_points,)),
        tf.keras.layers.Dense(512, activation="relu"),
        tf.keras.layers.Dense(256, activation="relu"),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dense(1, activation="sigmoid"),
    ])
    net.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
    return net

# Dataset sintetico mas grande: util para Colab con acelerador GPU.
_, X_big_raw, y_big = make_light_curves(n_samples=40000, n_points=128, noise=0.004)
X_big = scaler.transform(X_big_raw)

big_clf = build_large_classifier(X_big.shape[1])
t0 = time.perf_counter()
big_clf.fit(X_big, y_big, epochs=6, batch_size=1024, validation_split=0.2, verbose=0)
elapsed = time.perf_counter() - t0

print(f"Ejemplos usados: {len(X_big):,}")
print(f"Tiempo entrenamiento: {elapsed:.2f} s")
