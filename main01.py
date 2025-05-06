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

# 3. Crear múltiples agentes
agentes = []

# Agente Turista
turista = Agente("Turista", 0, 0, preferencias["Turistas"], umbral=5)
turista.decidir_mudanza(grid)
agentes.append(turista)

# Agente Residente Permanente
residente = Agente("ResidentePermanente", 19, 19, preferencias["Residentes permanentes"], umbral=5)
residente.decidir_mudanza(grid)
agentes.append(residente)

# 4. Decidir si se mueve
#print(f"Posición inicial: ({agente.x}, {agente.y})")
#agente.decidir_mudanza(grid)
#print(f"Posición final: ({agente.x}, {agente.y})")

# 5. Mostrar en pygame
#mostrar_simulacion(grid, [agente])
mostrar_simulacion(grid, agentes, tamaño_celda=30, velocidad=3)

