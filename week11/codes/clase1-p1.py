import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

tf.keras.utils.set_random_seed(42)

(x_train_full, y_train_full), (x_test, y_test) = keras.datasets.mnist.load_data()

# Escala de grises: enteros 0..255 -> flotantes 0..1.
x_train_full = x_train_full.astype("float32") / 255.0
x_test = x_test.astype("float32") / 255.0

# Separacion train/validation. Test queda reservado para el final.
x_train = x_train_full[:-10000]
y_train = y_train_full[:-10000]
x_val = x_train_full[-10000:]
y_val = y_train_full[-10000:]

print("train:", x_train.shape, y_train.shape)
print("val:  ", x_val.shape, y_val.shape)
print("test: ", x_test.shape, y_test.shape)

fig, axes = plt.subplots(2, 6, figsize=(8, 3))
for ax, img, label in zip(axes.ravel(), x_train[:12], y_train[:12]):
    ax.imshow(img, cmap="gray_r")
    ax.set_title(f"y={label}")
    ax.axis("off")
plt.tight_layout()
