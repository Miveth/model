import pygame
import numpy as np

COLOR_FONDO = (240, 240, 240)
COLOR_CELDA = (200, 200, 200)
COLOR_AGENTE = (255, 100, 100)
COLORES_AGENTES = {
    "Turista": (205, 133, 63),           # rojo
    "ResidentePermanente": (100, 100, 255), # azul
    "ResidenteSecundario": (100, 255, 100), # verde
    "Excursionista": (255, 255, 100)       # amarillo
}

def mostrar_simulacion(grid, agentes, tamaño_celda=40, velocidad=1):
    filas = grid.filas
    columnas = grid.columnas
    ancho = columnas * tamaño_celda
    alto = filas * tamaño_celda + 80

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

            # Mostrar info en pantalla (score en tiempo real)
            if hasattr(agente, "evaluaciones"):
                for (ex, ey, score, ok) in agente.evaluaciones:
                    if (ex, ey) == (agente.x, agente.y):
                        texto1 = fuente.render(f"Evaluando celda: ({ex},{ey})", True, (0, 0, 0))
                        texto2 = fuente.render(f"Score: {score} | Umbral: {agente.umbral}", True, (0, 0, 0))
                        texto3 = fuente.render(f"{'✅ Satisfecho' if ok else '❌ No cumple'}", True, (0, 150, 0) if ok else (200, 0, 0))

                        pantalla.blit(texto1, (10, filas * tamaño_celda + 5))
                        pantalla.blit(texto2, (10, filas * tamaño_celda + 25))
                        pantalla.blit(texto3, (10, filas * tamaño_celda + 45))
                        break

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
