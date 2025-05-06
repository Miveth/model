# main.py
from prefences import charge_preferences
from grid import Grid
from agente1 import Agente
from visualizacion1 import mostrar_simulacion

# 1. Cargar preferencias
path = "matriz_preferencias_agentes.csv"
preferencias, factores = charge_preferences(path)
num_factores = len(factores)

# 2. Crear el mapa
grid = Grid(20, 20, num_factores)

# 3. Crear un agente (tipo: turista)
pesos = preferencias["Turistas"]
umbral = 5
x, y = 0, 0
agente = Agente("Turista", x, y, pesos, umbral)

# 4. Decidir si se mueve
print(f"Posición inicial: ({agente.x}, {agente.y})")
agente.decidir_mudanza(grid)
print(f"Posición final: ({agente.x}, {agente.y})")

# 5. Mostrar en pygame
#mostrar_simulacion(grid, [agente])
mostrar_simulacion(grid, [agente], tamaño_celda=30, velocidad=3)

