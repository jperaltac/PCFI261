persona = pd.DataFrame(
    [
        {
            "Pregnancies": 1,
            "Glucose": 115,
            "BloodPressure": 72,
            "SkinThickness": 25,
            "Insulin": 90,
            "BMI": 28.5,
            "DiabetesPedigreeFunction": 0.35,
            "Age": 32,
        }
    ]
)

persona_s = preprocess.transform(persona[feature_names])
probabilidad = best_model.predict(persona_s, verbose=0).ravel()[0]

print(f"Probabilidad estimada por el modelo: {probabilidad:.3f}")
print(f"Porcentaje aproximado: {100 * probabilidad:.1f}%")
