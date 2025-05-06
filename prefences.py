# preferencias.py
import pandas as pd

def charge_preferences(path):
    """
    Lee el archivo CSV de preferencias y devuelve un diccionario de pesos por tipo de agente.
    """
    df = pd.read_csv(path)
    tipos = df.columns[1:]  # omite la primera columna (Factor)
    preferencias = {}

    for tipo in tipos:
        preferencias[tipo.strip()] = df[tipo].values.tolist()

    return preferencias, df['Factor'].tolist()

    '''
        retorna los objetos de la siguiente forma:
        {
        'Residentes permanentes': [0.5, 1.0, 0.8, ..., 0.6],
        'Turistas': [1.0, 0.3, 0.6, ..., 0.7],
        ...
        }
    '''