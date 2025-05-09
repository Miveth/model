# agente.py
import numpy as np
import random

class Agente:
    def __init__(self, unique_id, tipo, x, y, pesos, umbral):
        """
        tipo: tipo de agente (ej: 'Turista')
        x, y: posición inicial del agente en la malla
        pesos: lista de 12 valores que indican qué tan importante es cada factor
        umbral: puntuación mínima que acepta para quedarse en una celda
        """
        self.unique_id = unique_id
        self.tipo = tipo
        self.x = x
        self.y = y
        self.pesos = pesos
        self.umbral = umbral

    def evaluar_celda(self, atributos_celda):
        """
        calcula la satisfacción total de un agente respecto a una celda
        Calcula la puntuación de la celda actual según los pesos del agente.
        esto se hace con producto punto entre el vector de pesos y el vector de atributos de la celda

        Si tienes:

        Atributos de la celda:
        A = [a₁, a₂, a₃, ..., a₁₂] ← valores entre 0 y 1

        Preferencias del agente (pesos):
        P = [p₁, p₂, p₃, ..., p₁₂] ← valores también entre 0 y 1

        La puntuación que obtiene esa celda es:

        Puntuación = Σ(aᵢ * pᵢ) para i = 1 a 12
        puntuacion = a1*p1 + a2*p2 + a3*p3 + ... + a12*p12
        puntuacion = np.dot(atributos_celda, self.pesos)
        """
        puntuacion = np.dot(self.pesos, atributos_celda)
        return puntuacion

    def decidir_mudanza(self, grid):
        actual = grid.get_atributos(self.x, self.y)
        score_actual = self.evaluar_celda(actual)

        self.ruta = [(self.x, self.y)]
        self.evaluaciones = [(self.x, self.y, round(score_actual, 2), score_actual >= self.umbral)]
        self.evaluacion_actual = (self.x, self.y, round(score_actual, 2), score_actual >= self.umbral)

        posicion_actual = (self.x, self.y)

        if score_actual < self.umbral:
            for intento in range(50):
                nx, ny = grid.coordenadas_aleatorias()
                destino = (nx, ny)

                # Calcular ruta paso a paso
                pasos = self._calcular_ruta(posicion_actual, destino)
                for paso in pasos:
                    atributos = grid.get_atributos(*paso)
                    score = self.evaluar_celda(atributos)
                    self.ruta.append(paso)
                    self.evaluaciones.append((paso[0], paso[1], round(score, 2), score >= self.umbral))

                # Evaluar destino final
                atributos_final = grid.get_atributos(*destino)
                score_final = self.evaluar_celda(atributos_final)
                self.evaluacion_actual = (destino[0], destino[1], round(score_final, 2), score_final >= self.umbral)

                print(f"Intento {intento + 1}: {destino} → score {round(score_final, 2)}")

                if score_final >= self.umbral:
                    print(f"✅ ¡Celda adecuada encontrada en {destino} con score {round(score_final, 2)}!")
                    return

                posicion_actual = destino

        # si no encontró, ruta ya está acumulada


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
