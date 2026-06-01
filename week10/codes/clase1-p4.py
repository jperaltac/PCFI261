import time

print("Dispositivos disponibles:")
for device in tf.config.list_physical_devices():
    print(" -", device.name, device.device_type)

def build_regressor(width=256):
    net = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(5,)),
        tf.keras.layers.Dense(width, activation="relu"),
        tf.keras.layers.Dense(width, activation="relu"),
        tf.keras.layers.Dense(width, activation="relu"),
        tf.keras.layers.Dense(1),
    ])
    net.compile(optimizer="adam", loss="mse")
    return net

# Repetimos ejemplos para crear una carga matricial mas grande.
factor = 8
X_big = np.tile(X_train_s, (factor, 1))
y_big = np.tile(y_train, factor)

net = build_regressor(width=256)
t0 = time.perf_counter()
net.fit(X_big, y_big, epochs=8, batch_size=1024, verbose=0)
elapsed = time.perf_counter() - t0

print(f"Ejemplos usados: {len(X_big):,}")
print(f"Tiempo entrenamiento: {elapsed:.2f} s")
