# Guia docente breve

## Titulo sugerido

IA informada por fisica desde imagenes: recuperar la ecuacion de un proyectil.

## Objetivo de aprendizaje

Que el estudiantado conecte una observacion visual con una trayectoria numerica, un modelo neuronal y una restriccion fisica expresada como ecuacion diferencial.

## Secuencia sugerida de 2 clases

### Clase 1: de imagenes a datos y de datos a una red neuronal

1. Presentar el problema: una pelota se mueve bajo gravedad y se observa mediante una secuencia de imagenes.
2. Abrir `01_extraccion_trayectoria.ipynb`.
3. Detectar la pelota roja por segmentacion simple.
4. Convertir pixeles a metros usando la escala de la escena.
5. Guardar `trajectory_extracted.csv`.
6. Abrir `02_aprendizaje_con_red_neuronal.ipynb`.
7. Entrenar un perceptron multicapa con `tensorflow.keras` para aprender `x(t), y(t)` sin imponer una forma polinomial.
8. Comparar la prediccion con los datos y estimar la curvatura vertical usando `tf.GradientTape`.

Preguntas para discutir:

- Que supuestos aparecen al convertir pixeles a metros?
- Por que un detector simple basta en un caso controlado?
- Que cambia al usar una red neuronal en vez de ajustar directamente una parabola?
- Interpolar bien implica necesariamente recuperar una ley fisica?

### Clase 2: red neuronal informada por fisica y cierre del curso

1. Abrir `03_red_informada_por_fisica.ipynb`.
2. Definir una red `y_theta(t)` y un parametro aprendible `g`.
3. Construir una perdida con dos partes: error contra datos y residuo fisico `d²y/dt² + g`.
4. Entrenar el modelo con TensorFlow/Keras, usando `tf.GradientTape` para derivadas y gradientes.
5. Comparar el valor aprendido de `g` con el valor esperado.
6. Discutir por que incorporar estructura fisica puede mejorar interpretabilidad y extrapolacion.
7. Cerrar el curso conectando este laboratorio con el ciclo completo: datos, modelo, validacion, interpretacion y comunicacion.

Preguntas para discutir:

- Como cambia la solucion cuando la perdida incluye una ley fisica?
- Que representa el parametro `g` aprendido?
- Que ventajas y riesgos tiene una red informada por fisica frente a un modelo analitico simple?
- Como se podria adaptar esta idea a un pendulo, una orbita o un sistema con roce?

## Extension con video real

Para pasar a un video real:

1. Grabar con camara fija.
2. Usar fondo contrastante.
3. Lanzar una pelota de color intenso.
4. Incluir una regla, una cinta o una distancia conocida como escala.
5. Extraer frames con `ffmpeg`.
6. Reemplazar los archivos en `data/frames/`.

```bash
ffmpeg -i video_real.mp4 -vf fps=20 data/frames/frame_%03d.png
```

## Comentario pedagogico

Este laboratorio no busca usar una IA compleja. Busca instalar una idea moderna: la IA y el ajuste de datos son mas utiles en ciencia cuando se combinan con estructura fisica, unidades, validacion e interpretacion.
