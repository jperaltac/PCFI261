import numpy as np
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow import keras
from tensorflow.keras import layers


def make_synthetic_catalog(n_samples=4000, seed=261):
    rng = np.random.default_rng(seed)

    depth = rng.uniform(0.001, 0.03, n_samples)
    duration = rng.uniform(0.4, 12.0, n_samples)
    snr = rng.uniform(3.0, 60.0, n_samples)
    color = rng.uniform(0.2, 1.7, n_samples)
    variability = rng.uniform(0.0, 0.08, n_samples)

    X = np.column_stack([depth, duration, snr, color, variability])

    score = (
        22.0 * depth
        + 0.035 * snr
        - 0.11 * np.abs(duration - 4.5)
        - 5.5 * variability
        - 0.8 * np.maximum(color - 1.2, 0.0)
        + rng.normal(0.0, 0.18, n_samples)
    )
    y = (score > 0.55).astype(int)
    return X, y


X, y = make_synthetic_catalog()

X_train, X_temp, y_train, y_temp = train_test_split(
    X, y, test_size=0.30, random_state=261, stratify=y
)
X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp, test_size=0.50, random_state=261, stratify=y_temp
)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_val = scaler.transform(X_val)
X_test = scaler.transform(X_test)

model = keras.Sequential(
    [
        layers.Input(shape=(X_train.shape[1],)),
        layers.Dense(32, activation="relu"),
        layers.Dense(16, activation="relu"),
        layers.Dropout(0.15),
        layers.Dense(1, activation="sigmoid"),
    ]
)

model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=1e-3),
    loss="binary_crossentropy",
    metrics=["accuracy"],
)

callbacks = [
    keras.callbacks.EarlyStopping(
        monitor="val_loss",
        patience=12,
        restore_best_weights=True,
    )
]

history = model.fit(
    X_train,
    y_train,
    validation_data=(X_val, y_val),
    epochs=120,
    batch_size=64,
    verbose=0,
    callbacks=callbacks,
)

test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
print(f"test_loss={test_loss:.4f}")
print(f"test_accuracy={test_acc:.4f}")

proba = model.predict(X_test, verbose=0).ravel()
y_pred = (proba >= 0.5).astype(int)

print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred, digits=3))

# Algunas curvas utiles para graficar:
train_loss = history.history["loss"]
val_loss = history.history["val_loss"]
train_acc = history.history["accuracy"]
val_acc = history.history["val_accuracy"]

print("epochs usados:", len(train_loss))
print("ultimas losses:", train_loss[-3:], val_loss[-3:])
