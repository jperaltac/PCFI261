X, y = make_moons(n_samples=1200, noise=0.22, random_state=42)

print("Forma de X:", X.shape)
print("Forma de y:", y.shape)
print("Primeras 5 etiquetas:", y[:5])

plt.figure(figsize=(6, 5))
plt.scatter(X[:, 0], X[:, 1], c=y, cmap="coolwarm", s=18, edgecolor="k", alpha=0.8)
plt.xlabel("x1")
plt.ylabel("x2")
plt.title("Dataset sintético: two moons")
plt.show()

X_train_full, X_test, y_train_full, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

X_train, X_val, y_train, y_val = train_test_split(
    X_train_full, y_train_full, test_size=0.25, random_state=42, stratify=y_train_full
)

print("Entrenamiento:", X_train.shape, y_train.shape)
print("Validación:", X_val.shape, y_val.shape)
print("Prueba:", X_test.shape, y_test.shape)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)

print("Media aproximada del training escalado:", X_train_scaled.mean(axis=0))
print("Desviación estándar aproximada del training escalado:", X_train_scaled.std(axis=0))
