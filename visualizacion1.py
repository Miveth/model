import pygame
import numpy as np
from grafica_puntos import crear_grafica_scores_intentos
import matplotlib.pyplot as plt
import io
from grafica_puntos import crear_grafica_scores_dinamica

COLOR_FONDO = (240, 240, 240)
COLOR_CELDA = (200, 200, 200)
COLOR_AGENTE = (255, 100, 100)
COLORES_AGENTES = {
    "Turistas": (205, 133, 63),           # rojo
    "Residentes permanentes": (100, 100, 255), # azul
    "Residentes secundarios": (100, 255, 100), # verde
    "Excursionista": (255, 255, 100)       # amarillo
}

def mostrar_simulacion(grid, agentes, tamaño_celda=40, velocidad=1):
    filas = grid.filas
    columnas = grid.columnas
    ancho = columnas * tamaño_celda + 500
    alto = filas * tamaño_celda + 100

    pygame.init()
    pantalla = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("Simulación de Agentes - Pygame")
    reloj = pygame.time.Clock()
    fuente = pygame.font.SysFont('Arial', 18)

    # 🔽 Cargar imágenes después de pygame.init()
    iconos = {
        "mar": pygame.image.load("assets/mar.png"),
        "hotel": pygame.image.load("assets/hotel.png"),
        "escuela": pygame.image.load("assets/escuela1.png"),
        "parque": pygame.image.load("assets/parque.png"),
        "casa": pygame.image.load("assets/casa.png")
    }

    paso = 0
    corriendo = True

    headers = [
                "Agente",
                "Celda",
                "Score",
                 "Umbral",
                 "Estado"
             ]

    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

        pantalla.fill(COLOR_FONDO)

        # 🎨 Dibujar la malla con íconos
        for i in range(filas):
            for j in range(columnas):
                pygame.draw.rect(
                    pantalla,
                    COLOR_CELDA,
                    (j * tamaño_celda, i * tamaño_celda, tamaño_celda, tamaño_celda),
                    1
                )

                atributos = grid.get_atributos(i, j)
                tipo_icono = obtener_imagen_por_factor(atributos)

                if tipo_icono:
                    icono = pygame.transform.scale(iconos[tipo_icono], (tamaño_celda, tamaño_celda))
                    pantalla.blit(icono, (j * tamaño_celda, i * tamaño_celda))

       # 🔴 Dibujar agentes y texto
        mx, my = pygame.mouse.get_pos()
        hover_text = None
        
        # Dibujar encabezados
        for idx, header in enumerate(headers):
            texto_header = fuente.render(header, True, (0, 0, 0))
            pantalla.blit(texto_header, ((ancho - 480)+(idx*70), 20)) 

        for agente in agentes:
            if hasattr(agente, "ruta") and paso < len(agente.ruta):
                agente.x, agente.y = agente.ruta[paso]

            x_pix = agente.y * tamaño_celda
            y_pix = agente.x * tamaño_celda

            color = COLORES_AGENTES.get(agente.tipo, COLOR_AGENTE)

            pygame.draw.circle(
                pantalla, color,
                (x_pix + tamaño_celda // 2, y_pix + tamaño_celda // 2),
                tamaño_celda // 4
            ) 
             # 📌 Hover para mostrar información
            if x_pix <= mx <= x_pix + tamaño_celda and y_pix <= my <= y_pix + tamaño_celda:
                hover_text = f"{agente.tipo} - ({agente.x}, {agente.y})"
            
            # Mostrar info en pantalla (score en tiempo real) en formato tabla
            if hasattr(agente, "evaluaciones"):
                for (ex, ey, score, ok) in agente.evaluaciones:
                    if (ex, ey) == (agente.x, agente.y):
                        # Datos en formato tabla
                        datos = [
                            f"#{agente.unique_id}AG",  # El ID del agente
                            f"({ex},{ey})",
                            f"{score:.2f}",
                            f"{agente.umbral}",
                            "✅ Satisfecho" if ok else "❌ No cumple"
                        ]
                        
                        # Dibujar datos
                        for idx, dato in enumerate(datos):
                            # Color para el ID del agente (primera columna)
                            if idx == 0:
                                color = COLORES_AGENTES.get(agente.tipo, (0, 0, 0))  # Usa el color del agente
                            # Color para el estado (última columna)
                            elif idx == 4:
                                color = (0, 150, 0) if ok else (200, 0, 0)
                            # Color por defecto para el resto
                            else:
                                color = (0, 0, 0)
                                
                            texto_dato = fuente.render(dato, True, color)
                            pantalla.blit(texto_dato, ((ancho - 475)+(idx*70), 20 + (agente.unique_id * 20)))

                        # Mantener el nombre del agente en la parte inferior
                        texto_nombre = fuente.render(f"Agente#{agente.unique_id} (Tipo: {agente.tipo})", True, COLORES_AGENTES.get(agente.tipo, (0, 0, 0)) )
                        offset_y = (agente.unique_id - 1) * 20
                        pantalla.blit(texto_nombre, (10, filas * tamaño_celda + 5 + offset_y))
                        break

#       🖱️ Mostrar el hover si existe
        if hover_text:
            texto_hover = fuente.render(hover_text, True, (50, 50, 50))
            pantalla.blit(texto_hover, (mx + 15, my + 5))

        # Crear la gráfica dinámica y mostrarla en pygame
        buf = crear_grafica_scores_dinamica(agentes, paso, ventana=20, colores_agentes=COLORES_AGENTES)
        grafica_img = pygame.image.load(buf, 'grafica.png')
        pantalla.blit(grafica_img, (ancho - 480, 120))  # Ajusta la posición según tu layout

        # Dibuja la leyenda personalizada
        x_leyenda = ancho - 470  # Más a la izquierda (ajusta según tu layout)
        y_leyenda = 350          # Más abajo (ajusta según tu layout)
        for idx, agente in enumerate(agentes):
            color = COLORES_AGENTES.get(agente.tipo, (0, 0, 0))
            texto = fuente.render(f"Agente#{agente.unique_id}", True, color)
            pantalla.blit(texto, (x_leyenda, y_leyenda + idx * 25))

        pygame.display.flip()
        reloj.tick(velocidad)
        paso += 1

    pygame.quit()

def obtener_imagen_por_factor(valores_celda, umbral=0.8):
    """
    Dado un vector de atributos de una celda, devuelve el tipo de ícono a usar.
    Solo si el valor es mayor que cierto umbral.
    """
    etiquetas = {
        0: "mar",        # acceso al mar
        4: "hotel",      # infraestructura turística
        3: "escuela",    # servicios públicos
        8: "parque",     # estilo de vida
        10: "casa"       # disponibilidad inmobiliaria
    }

    for idx, nombre in etiquetas.items():
        if valores_celda[idx] >= umbral:
            return nombre
    return None
