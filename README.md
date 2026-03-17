# PCFI261 · Modelos Computacionales

Repositorio de material para el curso **PCFI261**, organizado por semanas en formato Beamer + ejemplos en Python.

## Estructura del repositorio

- `latex/`: preámbulo compartido para las presentaciones (`preamble-beamer.tex`).
- `week01/` a `week04/`: contenido semanal (diapositivas `notes.tex`, imágenes, scripts y Makefile).
- `scripts/build_site.py`: utilitario para construir el sitio estático.
- `site/`: versión HTML/CSS del índice del curso.

## Semana 04 (actualizada)

La semana 04 quedó alineada con el formato de semanas anteriores:

- Un solo PDF con división explícita en **Clase 1** y **Clase 2**.
- Distribución sugerida por clase: **30–45 min teoría + 75–90 min práctica**.
- Mayor cobertura conceptual de dinámica molecular.
- Nuevos ejemplos de código para:
  - integración de Euler;
  - paso `velocity Verlet` con fuerza de Lennard–Jones;
  - simulación de billar 2D con rebotes y gravedad.

## Compilación local de una semana

Desde la carpeta de la semana (ejemplo `week04/`):

```bash
make
```

Esto ejecuta `pdflatex` con `-shell-escape` para renderizar bloques `minted`.

Para limpiar archivos auxiliares:

```bash
make clean
```

## Requisitos recomendados

- `pdflatex` (TeX Live o similar)
- `python3`
- paquete LaTeX `minted`
- `pygments` (requerido por `minted`)

## Notas de estilo

- El formato de las semanas recientes usa el preámbulo común:
  - `\input{../latex/preamble-beamer.tex}`
- Se recomienda mantener esa convención para asegurar consistencia visual y tipográfica.
