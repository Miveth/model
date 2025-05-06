# grid.py
import numpy as np
import random

class Grid:
    def __init__(self, filas, columnas, num_factores):
        self.filas = filas
        self.columnas = columnas
        self.num_factores = num_factores

        # Malla de tamaño (filas x columnas x factores)
        self.matriz = np.random.rand(filas, columnas, num_factores)

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
