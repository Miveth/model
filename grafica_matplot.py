import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import copy

def animar_grid(grid, lista_agentes_por_paso, tipos=None, interval=500, nombre_archivo=None):
    """
    Crea una animación de la evolución del grid.
    - grid: el objeto Grid (para dimensiones)
    - lista_agentes_por_paso: lista de listas de agentes (uno por cada paso)
    - tipos: lista de tipos de agentes (opcional, se infiere si no se da)
    - interval: tiempo entre frames en ms
    - nombre_archivo: si se da, guarda el gif
    """
    filas, columnas = grid.filas, grid.columnas

    # Inferir tipos si no se pasan
    if tipos is None:
        tipos = list({agente.tipo for agentes in lista_agentes_por_paso for agente in agentes})
    tipo_a_num = {tipo: idx for idx, tipo in enumerate(tipos)}

    fig, ax = plt.subplots(figsize=(6,6))
    matriz = np.full((filas, columnas), -1)
    im = ax.imshow(matriz, cmap=plt.get_cmap('tab10', len(tipos)), vmin=-1, vmax=len(tipos)-1)
    cbar = plt.colorbar(im, ticks=range(len(tipos)))
    cbar.ax.set_yticklabels(tipos)
    ax.set_title("Evolución de la segregación")
    ax.set_xlabel("Y")
    ax.set_ylabel("X")

    def actualizar(frame):
        agentes = lista_agentes_por_paso[frame]
        matriz = np.full((filas, columnas), -1)
        for agente in agentes:
            matriz[agente.x, agente.y] = tipo_a_num[agente.tipo]
        im.set_data(matriz)
        ax.set_title(f"Paso {frame+1}")
        return [im]

    ani = animation.FuncAnimation(fig, actualizar, frames=len(lista_agentes_por_paso), interval=interval, blit=True)
    plt.tight_layout()
    if nombre_archivo:
        ani.save(nombre_archivo, writer='imagemagick')
    plt.show()
