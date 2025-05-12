# grafica_de_puntos.py
import matplotlib.pyplot as plt
import io

def crear_grafica_scores_intentos(agentes):
    """
    Genera una imagen PNG en memoria con la evolución de los scores de cada agente hasta el paso_actual.
    Retorna un buffer listo para cargar en pygame.
    """
    plt.figure(figsize=(4, 2))
    for agente in agentes:
        scores = agente.intentos  # Solo los intentos reales
        plt.plot(range(1, len(scores)+1), scores, marker='o', label=f'Agente#{agente.unique_id}')
    plt.xlabel('Intento')
    plt.ylabel('Score')
    plt.legend()
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='PNG')
    plt.close()
    buf.seek(0)
    return buf

def crear_grafica_scores_dinamica(agentes, paso_actual, ventana=20, colores_agentes=None):
    """
    Genera una imagen PNG en memoria con la evolución de los scores de cada agente hasta el paso_actual.
    Si hay más de 'ventana' intentos, solo muestra los últimos 'ventana'.
    La leyenda se coloca abajo.
    colores_agentes: diccionario {tipo: (R, G, B)} con los colores de cada agente
    """
    plt.figure(figsize=(4, 2))
    for agente in agentes:
        scores = agente.intentos[:paso_actual+1]
        if len(scores) > ventana:
            x = list(range(len(scores) - ventana + 1, len(scores) + 1))
            y = scores[-ventana:]
        else:
            x = list(range(1, len(scores) + 1))
            y = scores
        # Usa el color del agente si está disponible
        color = None
        if colores_agentes is not None:
            rgb = colores_agentes.get(agente.tipo, (0, 0, 0))
            # Normaliza a [0,1] para matplotlib
            color = tuple([v/255 for v in rgb])
        plt.plot(x, y, marker='o', label=f'Agente#{agente.unique_id}', color=color)
    plt.xlabel('Intento')
    plt.ylabel('Score')
    plt.tight_layout(rect=[0, 0.15, 1, 1])  # Deja espacio abajo para la leyenda, margenes, izquierdo 0, borde inferior 0.15, derecho 1, alto 1
    # plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.45), ncol=1)
    '''  plt.legend(
        loc='lower left',
        bbox_to_anchor=(-0.10, -1),  # Más a la izquierda y más abajo
        ncol=1
    )
    '''
    buf = io.BytesIO()
    plt.savefig(buf, format='PNG')
    plt.close()
    buf.seek(0)
    return buf
