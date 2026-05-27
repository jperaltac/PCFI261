from IPython.display import Image, display

def _dense_layers(model):
    return [layer for layer in model.layers if isinstance(layer, layers.Dense)]

def layer_sizes_from_keras(model, input_dim=None):
    if input_dim is None:
        try:
            input_shape = model.input_shape
            if isinstance(input_shape, list):
                input_shape = input_shape[0]
            input_dim = int(input_shape[-1])
        except Exception:
            input_dim = None

    sizes = []
    if input_dim is not None:
        sizes.append(int(input_dim))

    for layer in _dense_layers(model):
        sizes.append(int(layer.units))

    return sizes

def plot_network_architecture(
    layer_sizes,
    layer_labels=None,
    title="Arquitectura de la red",
    max_neurons=16,
    connection_alpha=0.18
):
    n_layers = len(layer_sizes)

    if layer_labels is None:
        layer_labels = [f"Capa {i}" for i in range(n_layers)]

    fig, ax = plt.subplots(figsize=(1.8 * n_layers + 2, 5.5))
    ax.set_title(title, fontsize=14)

    x_positions = np.linspace(0, n_layers - 1, n_layers)
    visible_positions = []

    for layer_idx, (x, n_neurons) in enumerate(zip(x_positions, layer_sizes)):
        n_visible = min(n_neurons, max_neurons)

        if n_visible == 1:
            y_positions = np.array([0.0])
        else:
            y_positions = np.linspace(-1.0, 1.0, n_visible)

        visible_positions.append((x, y_positions))

        for y_pos in y_positions:
            circle = plt.Circle(
                (x, y_pos),
                radius=0.055,
                fill=True,
                ec="black",
                lw=1.0,
                zorder=3
            )
            ax.add_patch(circle)

        if n_neurons > max_neurons:
            ax.text(
                x,
                -1.22,
                r"$\vdots$",
                ha="center",
                va="center",
                fontsize=18
            )
            shown_text = f"{n_visible} de {n_neurons} neuronas"
        else:
            shown_text = f"{n_neurons} neurona" if n_neurons == 1 else f"{n_neurons} neuronas"

        ax.text(
            x,
            1.28,
            layer_labels[layer_idx],
            ha="center",
            va="bottom",
            fontsize=10
        )
        ax.text(
            x,
            -1.42,
            shown_text,
            ha="center",
            va="top",
            fontsize=9
        )

    for layer_idx in range(n_layers - 1):
        x0, y0s = visible_positions[layer_idx]
        x1, y1s = visible_positions[layer_idx + 1]

        for y0 in y0s:
            for y1 in y1s:
                ax.plot(
                    [x0 + 0.055, x1 - 0.055],
                    [y0, y1],
                    lw=0.6,
                    alpha=connection_alpha,
                    zorder=1
                )

    ax.set_xlim(-0.5, n_layers - 0.5)
    ax.set_ylim(-1.65, 1.65)
    ax.axis("off")
    plt.show()

def plot_keras_architecture(model, input_dim=None, title=None, max_neurons=16):
    sizes = layer_sizes_from_keras(model, input_dim=input_dim)

    labels = ["Entrada"]
    for layer in _dense_layers(model):
        activation_name = getattr(layer.activation, "__name__", str(layer.activation))
        labels.append(f"{layer.name}\nDense({layer.units})\nact: {activation_name}")

    if title is None:
        title = f"Arquitectura: {model.name}"

    plot_network_architecture(
        sizes,
        layer_labels=labels,
        title=title,
        max_neurons=max_neurons
    )

def show_keras_graph(model, filename="keras_model.png"):
    try:
        keras.utils.plot_model(
            model,
            to_file=filename,
            show_shapes=True,
            show_layer_names=True,
            show_layer_activations=True,
            dpi=110
        )
        display(Image(filename))
    except Exception as exc:
        print("No se pudo usar keras.utils.plot_model.")
        print("Causa probable: falta pydot o Graphviz en el entorno.")
        print("Detalle técnico:", repr(exc))
        print("\nUsando visualización simple como respaldo:")
        plot_keras_architecture(model, input_dim=2)

def show_visualkeras(model):
    try:
        import visualkeras
        display(visualkeras.layered_view(model, legend=True))
    except ModuleNotFoundError:
        print("visualkeras no está instalado.")
        print("En Colab puedes ejecutar: !pip -q install visualkeras")
    except Exception as exc:
        print("visualkeras está instalado, pero no pudo dibujar el modelo.")
        print("Detalle técnico:", repr(exc))

def plot_keras_weight_heatmaps(model, title="Matrices de pesos aprendidas"):
    dense_layers = _dense_layers(model)

    if len(dense_layers) == 0:
        print("El modelo no tiene capas Dense para visualizar.")
        return

    fig, axes = plt.subplots(
        1,
        len(dense_layers),
        figsize=(4.2 * len(dense_layers), 3.6),
        squeeze=False
    )
    axes = axes.ravel()

    for ax, layer in zip(axes, dense_layers):
        weights = layer.get_weights()
        if len(weights) == 0:
            ax.axis("off")
            ax.set_title(f"{layer.name}\nsin pesos")
            continue

        W = weights[0]
        im = ax.imshow(W, aspect="auto")
        ax.set_title(f"{layer.name}\nW: {W.shape}")
        ax.set_xlabel("neurona destino")
        ax.set_ylabel("entrada")
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

    fig.suptitle(title)
    plt.tight_layout()
    plt.show()

def plot_hidden_neuron_maps(
    model,
    X_plot,
    layer_index=0,
    neurons=(0, 1, 2, 3),
    title="Mapas de activación de neuronas ocultas"
):
    dense_layers = _dense_layers(model)

    if layer_index >= len(dense_layers):
        print("layer_index fuera de rango.")
        return

    target_layer = dense_layers[layer_index]
    if target_layer.units < 1:
        print("La capa seleccionada no tiene neuronas.")
        return

    x_min, x_max = X_plot[:, 0].min() - 0.8, X_plot[:, 0].max() + 0.8
    y_min, y_max = X_plot[:, 1].min() - 0.8, X_plot[:, 1].max() + 0.8

    xx, yy = np.meshgrid(
        np.linspace(x_min, x_max, 180),
        np.linspace(y_min, y_max, 180)
    )

    grid = np.c_[xx.ravel(), yy.ravel()]
    grid_scaled = scaler.transform(grid)

    activation_model = keras.Model(
        inputs=model.inputs,
        outputs=target_layer.output
    )
    activations = activation_model.predict(grid_scaled, verbose=0)

    valid_neurons = [j for j in neurons if j < activations.shape[1]]
    if len(valid_neurons) == 0:
        print("Ninguna neurona solicitada existe en esa capa.")
        return

    fig, axes = plt.subplots(
        1,
        len(valid_neurons),
        figsize=(4.0 * len(valid_neurons), 3.6),
        squeeze=False
    )
    axes = axes.ravel()

    for ax, neuron_idx in zip(axes, valid_neurons):
        zz = activations[:, neuron_idx].reshape(xx.shape)
        contour = ax.contourf(xx, yy, zz, levels=30)
        ax.set_title(f"{target_layer.name}, neurona {neuron_idx}")
        ax.set_xlabel("x1")
        ax.set_ylabel("x2")
        fig.colorbar(contour, ax=ax, fraction=0.046, pad=0.04)

    fig.suptitle(title)
    plt.tight_layout()
    plt.show()

def plot_sklearn_mlp_architecture(clf, input_dim, title="Arquitectura MLPClassifier"):
    hidden = clf.hidden_layer_sizes
    if isinstance(hidden, int):
        hidden = [hidden]
    else:
        hidden = list(hidden)

    output_dim = int(getattr(clf, "n_outputs_", 1))
    sizes = [int(input_dim)] + [int(h) for h in hidden] + [output_dim]

    labels = ["Entrada"]
    labels += [f"Oculta {i + 1}\n{h} neuronas" for i, h in enumerate(hidden)]
    labels += ["Salida"]

    plot_network_architecture(
        sizes,
        layer_labels=labels,
        title=title,
        max_neurons=16
    )

def plot_decision_boundary_sklearn(model, X_plot, y_plot, title="Frontera de decisión"):
    x_min, x_max = X_plot[:, 0].min() - 0.8, X_plot[:, 0].max() + 0.8
    y_min, y_max = X_plot[:, 1].min() - 0.8, X_plot[:, 1].max() + 0.8

    xx, yy = np.meshgrid(
        np.linspace(x_min, x_max, 300),
        np.linspace(y_min, y_max, 300)
    )

    grid = np.c_[xx.ravel(), yy.ravel()]
    grid_scaled = scaler.transform(grid)

    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(grid_scaled)[:, 1].reshape(xx.shape)
    else:
        probs = model.predict(grid_scaled).reshape(xx.shape)

    plt.figure(figsize=(6, 5))
    plt.contourf(xx, yy, probs, levels=30, cmap="coolwarm", alpha=0.55)
    plt.contour(xx, yy, probs, levels=[0.5], colors="black", linewidths=2)
    plt.scatter(X_plot[:, 0], X_plot[:, 1], c=y_plot, cmap="coolwarm", s=18, edgecolor="k")
    plt.xlabel("x1")
    plt.ylabel("x2")
    plt.title(title)
    plt.show()
