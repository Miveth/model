# grid.py
import numpy as np
import random

class Grid:
    def __init__(self, filas, columnas, num_factores):
        self.filas = filas
        self.columnas = columnas
        self.num_factores = num_factores

        # Inicializa la malla con ceros (sin ruido aleatorio)
        self.matriz = np.zeros((filas, columnas, num_factores))

    def get_atributos(self, x, y):
        """
        Devuelve los atributos (vector de factores) de la celda (x, y).
        """
        return self.matriz[x, y]

    def coordenadas_aleatorias(self):
        """
        Devuelve una tupla (x, y) aleatoria dentro de la malla.
        """
        x = random.randint(0, self.filas - 1)
        y = random.randint(0, self.columnas - 1)
        return x, y

    def get_agentes_en_celda(self, x, y):
        """Retorna la lista de agentes en la celda (x,y)"""
        # Implementar según tu estructura de datos actual
        pass

    def celda_vacia(self, x, y, agentes):
        """Devuelve True si no hay ningún agente en la celda (x, y)"""
        for agente in agentes:
            if agente.x == x and agente.y == y:
                return False
        return True

    def asignar_region(self, x0, y0, ancho, alto, factor_idx, valor):
        """
        Asigna un valor a un factor específico en una región rectangular.
        x0, y0: esquina superior izquierda
        ancho, alto: dimensiones de la región
        factor_idx: índice del factor a modificar (ej: 0 para mar)
        valor: valor a asignar (ej: 1.0 para presencia total)
        """
        for i in range(x0, x0 + alto):
            for j in range(y0, y0 + ancho):
                if 0 <= i < self.filas and 0 <= j < self.columnas:
                    self.matriz[i, j, factor_idx] = valor
