from PIL import Image, ImageOps

def preparar_numero(path, mostrar=True):
    """Convierte una foto de un digito a una imagen tipo MNIST."""
    img = Image.open(path).convert("L")

    # MNIST tiene digitos claros sobre fondo oscuro. Si la foto viene al reves,
    # invertimos usando el brillo medio como criterio simple.
    if np.asarray(img).mean() > 127:
        img = ImageOps.invert(img)

    img.thumbnail((20, 20), Image.Resampling.LANCZOS)
    canvas = Image.new("L", (28, 28), color=0)
    left = (28 - img.width) // 2
    top = (28 - img.height) // 2
    canvas.paste(img, (left, top))

    arr = np.asarray(canvas).astype("float32") / 255.0
    if mostrar:
        plt.imshow(arr, cmap="gray_r")
        plt.axis("off")
        plt.show()
    return arr

# En Colab se puede subir una foto con:
# from google.colab import files
# files.upload()
#
# Luego cambiar el nombre del archivo:
mi_numero = preparar_numero("mi_numero.jpg")

prob = cnn_model.predict(mi_numero[np.newaxis, ..., np.newaxis], verbose=0)[0]
pred = int(np.argmax(prob))
print("prediccion:", pred)
print("confianza aproximada:", prob[pred])
