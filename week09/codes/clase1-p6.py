print("Resumen comparativo")
print("-" * 40)
print(f"Accuracy test modelo lineal    : {test_acc_linear:.4f}")
print(f"Accuracy test modelo no lineal : {test_acc_nl:.4f}")

y_pred_prob = nonlinear_model.predict(X_test_scaled, verbose=0).ravel()
y_pred = (y_pred_prob >= 0.5).astype(int)

print("Matriz de confusión")
print(confusion_matrix(y_test, y_pred))

print("\nReporte de clasificación")
print(classification_report(y_test, y_pred, digits=4))

indices = np.random.choice(len(X_test), size=10, replace=False)

for idx in indices:
    x_original = X_test[idx]
    x_scaled = X_test_scaled[idx:idx+1]
    prob = nonlinear_model.predict(x_scaled, verbose=0)[0, 0]
    pred = int(prob >= 0.5)
    truth = int(y_test[idx])
    print(f"x = {x_original}, prob(clase 1) = {prob:.3f}, pred = {pred}, real = {truth}")
