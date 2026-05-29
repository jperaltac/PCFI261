best_name = pd.DataFrame(results).sort_values("val_auc", ascending=False).iloc[0]["modelo"]
best_model = trained_models[best_name]

proba_test = best_model.predict(X_test_s, verbose=0).ravel()
y_pred_05 = (proba_test >= 0.5).astype(int)

print("modelo elegido:", best_name)
print("AUC test:", roc_auc_score(y_test, proba_test))
print(confusion_matrix(y_test, y_pred_05))
print(classification_report(y_test, y_pred_05, digits=3))

thresholds = [0.3, 0.5, 0.7]
threshold_rows = []

for threshold in thresholds:
    y_pred = (proba_test >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
    threshold_rows.append(
        {
            "threshold": threshold,
            "TN": tn,
            "FP": fp,
            "FN": fn,
            "TP": tp,
            "sensibilidad": tp / (tp + fn),
            "especificidad": tn / (tn + fp),
        }
    )

pd.DataFrame(threshold_rows)
