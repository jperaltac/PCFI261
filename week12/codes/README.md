# Semana 12 - IA informada por fisica desde imagenes: lanzamiento de proyectil

Este paquete contiene el laboratorio final de PCFI261. La idea es cerrar el curso con un flujo completo de modelamiento computacional:

1. pasar desde imagenes a datos;
2. entrenar una red neuronal con TensorFlow/Keras;
3. incorporar una ley fisica en la funcion de perdida para estimar `g`.

El material mantiene continuidad con las semanas anteriores, donde se trabajo con Keras y TensorFlow.

## Estructura

- `data/frames/`: imagenes sinteticas generables por `scripts/generate_assets.py`.
- `data/projectile_synthetic.mp4`: video simple generado si `ffmpeg` esta disponible.
- `data/ground_truth.csv`: trayectoria exacta usada para crear las imagenes.
- `data/trajectory_extracted.csv`: trayectoria recuperada desde los frames sinteticos.
- `notebooks/01_extraccion_trayectoria.ipynb`: extrae posiciones desde imagenes.
- `notebooks/02_aprendizaje_con_red_neuronal.ipynb`: entrena una red neuronal con `tensorflow.keras` para modelar `x(t), y(t)` sin imponer una forma polinomial.
- `notebooks/03_red_informada_por_fisica.ipynb`: entrena una red informada por fisica usando `tf.GradientTape` para penalizar el residuo `d²y/dt² + g`.
- `scripts/generate_assets.py`: regenera datos, frames y video.

## Flujo pedagogico sugerido

1. Usar el notebook 01 para pasar de imagenes a una tabla con `t`, `x` e `y`.
2. Abrir el notebook 02 para entrenar una red neuronal que aprenda la trayectoria sin asumir la ecuacion parabola desde el inicio.
3. Usar diferenciacion automatica de TensorFlow para estimar la curvatura vertical aprendida por la red.
4. Abrir el notebook 03 para entrenar una red neuronal informada por fisica, donde la perdida combina ajuste a datos y cumplimiento de la ecuacion del movimiento.
5. Comparar la red libre con la red informada por fisica y discutir interpretabilidad, extrapolacion y rol de las leyes fisicas.

## Dependencias

```bash
pip install -r requirements.txt
```

Para regenerar los datos sinteticos, frames y video:

```bash
python scripts/generate_assets.py
```

## Extension natural

Luego se puede reemplazar `data/frames/` por frames extraidos desde un video real grabado con celular. Lo importante es conservar un objeto facil de segmentar, una camara fija y una escala conocida en la escena.
