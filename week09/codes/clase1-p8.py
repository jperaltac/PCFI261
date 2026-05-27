from sklearn.neural_network import MLPClassifier

mlp_sklearn = MLPClassifier(
    hidden_layer_sizes=(16, 16),
    activation="tanh",
    solver="adam",
    learning_rate_init=0.01,
    max_iter=2000,
    random_state=42
)

mlp_sklearn.fit(X_train_scaled, y_train)

plot_sklearn_mlp_architecture(
    mlp_sklearn,
    input_dim=2,
    title="Arquitectura de una red MLPClassifier de scikit-learn"
)

print(f"Accuracy test MLPClassifier: {mlp_sklearn.score(X_test_scaled, y_test):.4f}")

plot_decision_boundary_sklearn(
    mlp_sklearn,
    X_test,
    y_test,
    title="MLPClassifier de scikit-learn sobre datos de prueba"
)
