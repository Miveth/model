# main.py
from prefences import charge_preferences
from grid import Grid
from agente1 import Agente
from visualizacion1 import mostrar_simulacion
import random
import numpy as np
import copy
from grafica_matplot import animar_grid

# 1. Cargar preferencias
path = "matriz_preferencias_agentes.csv"
preferencias, factores = charge_preferences(path)
num_factores = len(factores)

# 2. Crear el mapa
grid = Grid(20, 20, num_factores)

# 2.1 Poblar el mapa con regiones específicas
# Mar en la esquina superior izquierda (4x7)
grid.asignar_region(0, 0, 7, 4, factor_idx=0, valor=1.0)

# Asumiendo que los índices de factores son:
# 0: mar, 4: hotel, 3: escuela, 8: parque, 10: casa
# Mar en la esquina superior izquierda (4x7)
grid.asignar_region(0, 0, 7, 4, factor_idx=0, valor=1.0)

# Mar en la esquina inferior derecha (4x7)
grid.asignar_region(16, 13, 7, 4, factor_idx=0, valor=1.0)

# Mar en el centro (4x4)
grid.asignar_region(8, 8, 4, 4, factor_idx=0, valor=1.0)

# Hoteles alrededor del mar de la esquina superior izquierda
grid.asignar_region(0, 7, 2, 4, factor_idx=4, valor=1.0)  # Hoteles a la derecha del mar
grid.asignar_region(4, 0, 3, 2, factor_idx=4, valor=1.0)  # Hoteles debajo del mar

# Casas en el resto del mapa (valor bajo para no saturar)
grid.asignar_region(0, 0, 20, 20, factor_idx=10, valor=0.5)

# Escuelas cerca de casas (por ejemplo, en el centro)
grid.asignar_region(6, 6, 2, 2, factor_idx=3, valor=1.0)

# Parques en otra zona
grid.asignar_region(12, 2, 3, 3, factor_idx=8, valor=1.0)


# (Aquí puedes agregar más regiones si quieres...)

# 3. Crear múltiples agentes
agentes = []

# Configuración de agentes por tipo
config_agentes = {
    "Turistas": {
        "cantidad": 50,
        "pos_inicial": (0, 0),
        "umbral": 1,
        "tolerancia": 0.3
    },
    "Residentes permanentes": {
        "cantidad": 53,
        "pos_inicial": (19, 19),
        "umbral": 0.5,
        "tolerancia": 0.4
    },
    "Residentes secundarios": {
        "cantidad": 34,
        "pos_inicial": (19, 0),
        "umbral": 0.8,
        "tolerancia": 0.35
    }
}

# Crear agentes de cada tipo
id_actual = 1
for tipo, config in config_agentes.items():
    for i in range(config["cantidad"]):
        # Buscar una celda vacía para el agente
        while True:
            x, y = config["pos_inicial"]
            # Puedes randomizar la posición inicial si quieres más dispersión
            x, y = random.randint(0, grid.filas-1), random.randint(0, grid.columnas-1)
            if grid.celda_vacia(x, y, agentes):
                break
        agente = Agente(
            unique_id=id_actual,
            tipo=tipo,
            x=x,
            y=y,
            pesos=preferencias[tipo],
            umbral=config["umbral"],
            tolerancia=config["tolerancia"]
        )
        
        # Decidir mudanza para el agente
        agente.decidir_mudanza(grid, agentes)
        
        # Agregar a la lista de agentes
        agentes.append(agente)
        
        # Incrementar ID para el siguiente agente
        id_actual += 1

# 4. Mostrar en pygame
#mostrar_simulacion(grid, agentes, tamaño_celda=30, velocidad=3)


''' para crear en otro main o solo probar la grafica poner en otro main
import copy
from grafica_matplot import animar_grid
'''

num_pasos = 20  # Puedes ajustar el número de pasos
historial_agentes = []

for paso in range(num_pasos):
    for agente in agentes:
        agente.decidir_mudanza(grid, agentes)
    historial_agentes.append(copy.deepcopy(agentes))

# Animación con matplotlib
animar_grid(grid, historial_agentes)

# (Opcional) Visualización en Pygame
# mostrar_simulacion(grid, agentes, tamaño_celda=30, velocidad=3)

# Asumiendo que los índices de factores son:
# 0: mar, 4: hotel, 3: escuela, 8: parque, 10: casa

# Mar en la esquina superior izquierda (4x7)
#grid.asignar_region(0, 0, 7, 4, factor_idx=0, valor=1.0)

# Mar en la esquina inferior derecha (4x7)
#mostrar_simulacion(grid, agentes, tamaño_celda=30, velocidad=3)