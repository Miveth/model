# agente.py
import numpy as np
import random

class Agente:
    def __init__(self, unique_id, tipo, x, y, pesos, umbral, tolerancia=0.3):
        """
        tipo: tipo de agente (ej: 'Turista')
        x, y: posición inicial del agente en la malla
        pesos: lista de 12 valores que indican qué tan importante es cada factor
        umbral: puntuación mínima que acepta para quedarse en una celda
        tolerancia: proporción máxima de vecinos diferentes que tolera (0-1)
        """
        self.unique_id = unique_id
        self.tipo = tipo
        self.x = x
        self.y = y
        self.pesos = pesos
        self.umbral = umbral
        self.tolerancia = tolerancia
        self.intentos = []
        self.satisfecho_vecindario = False

    def evaluar_vecindario(self, grid, x, y):
        """
        Evalúa la composición del vecindario (8 celdas alrededor)
        Retorna: (proporción_similares, proporción_diferentes)
        """
        similares = 0
        diferentes = 0
        total_vecinos = 0
        
        # Revisar las 8 celdas vecinas
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                    
                nx, ny = x + dx, y + dy
                if not (0 <= nx < grid.filas and 0 <= ny < grid.columnas):
                    continue
                
                # Obtener agentes en la celda vecina
                vecinos = grid.get_agentes_en_celda(nx, ny)
                if not vecinos:  # Celda vacía
                    continue
                    
                total_vecinos += 1
                for vecino in vecinos:
                    if vecino.tipo == self.tipo:
                        similares += 1
                    else:
                        diferentes += 1
        
        if total_vecinos == 0:
            return 1.0, 0.0  # No hay vecinos, consideramos que es un buen vecindario
            
        return similares/total_vecinos, diferentes/total_vecinos

    def evaluar_celda(self, atributos_celda, grid=None):
        """
        Calcula la satisfacción total de un agente respecto a una celda
        Ahora incluye tanto los atributos de la celda como la composición del vecindario
        """
        # Evaluación base de la celda
        puntuacion_base = np.dot(self.pesos, atributos_celda)
        
        # Si no tenemos grid o no estamos evaluando una posición específica,
        # retornamos solo la puntuación base
        if grid is None:
            return puntuacion_base
            
        # Evaluar el vecindario
        similares, diferentes = self.evaluar_vecindario(grid, self.x, self.y)
        
        # Ajustar la puntuación según la composición del vecindario
        if diferentes > self.tolerancia:
            # Reducir la puntuación si hay demasiados vecinos diferentes
            factor_vecindario = 1 - (diferentes - self.tolerancia)
            puntuacion_base *= factor_vecindario
            self.satisfecho_vecindario = False
        else:
            self.satisfecho_vecindario = True
            
        return puntuacion_base

    def decidir_mudanza(self, grid, agentes):
        actual = grid.get_atributos(self.x, self.y)
        score_actual = self.evaluar_celda(actual, grid)

        self.ruta = [(self.x, self.y)]
        self.evaluaciones = [(self.x, self.y, round(score_actual, 2), 
                            score_actual >= self.umbral and self.satisfecho_vecindario)]
        self.evaluacion_actual = (self.x, self.y, round(score_actual, 2), 
                                score_actual >= self.umbral and self.satisfecho_vecindario)

        posicion_actual = (self.x, self.y)
        self.intentos = []

        # Moverse si no está satisfecho con la celda O con el vecindario
        if score_actual < self.umbral or not self.satisfecho_vecindario:
            for intento in range(50):
                nx, ny = grid.coordenadas_aleatorias()
                # Solo considerar celdas vacías
                if not grid.celda_vacia(nx, ny, agentes):
                    continue

                destino = (nx, ny)
                pasos = self._calcular_ruta(posicion_actual, destino)
                for paso in pasos:
                    if not grid.celda_vacia(paso[0], paso[1], agentes):
                        break  # No seguir si el camino está ocupado
                    self.x, self.y = paso
                    atributos = grid.get_atributos(*paso)
                    score = self.evaluar_celda(atributos, grid)
                    self.ruta.append(paso)
                    self.evaluaciones.append((paso[0], paso[1], round(score, 2), 
                                           score >= self.umbral and self.satisfecho_vecindario))

                # Evaluar destino final
                self.x, self.y = destino  # Actualizar posición temporalmente
                atributos_final = grid.get_atributos(*destino)
                score_final = self.evaluar_celda(atributos_final, grid)
                self.evaluacion_actual = (destino[0], destino[1], round(score_final, 2), 
                                        score_final >= self.umbral and self.satisfecho_vecindario)

                self.intentos.append(score_final)

                print(f"Intento {intento + 1}: {destino} → score {round(score_final, 2)} " +
                      f"(Vecindario: {'✅' if self.satisfecho_vecindario else '❌'})")

                if score_final >= self.umbral and self.satisfecho_vecindario:
                    print(f"✅ ¡Celda adecuada encontrada en {destino} con score {round(score_final, 2)}!")
                    return

                posicion_actual = destino

        # Restaurar posición original si no se encontró una mejor
        self.x, self.y = posicion_actual

    def _calcular_ruta(self, inicio, fin):
        ruta = []
        x0, y0 = inicio
        x1, y1 = fin

        while x0 != x1:
            x0 += 1 if x0 < x1 else -1
            ruta.append((x0, y0))
        while y0 != y1:
            y0 += 1 if y0 < y1 else -1
            ruta.append((x0, y0))

        return ruta

