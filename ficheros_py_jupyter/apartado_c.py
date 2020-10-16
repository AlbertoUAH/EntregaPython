"""
@author: alberto
"""
import apartado_b
import pandas as pd

# apartado c)
def generar_tabla_poblacion(datos_poblacion, fecha_ini, fecha_fin, pais = "all"):
    """
    Funcion que permite generar una tabla, en formato DataFrame, 
    con las poblaciones del pais pasado como parametro, entre dos annos dados. 
    AVISO: Devuelve DataFrame vacio si no encuentran coincidencias. 
    Si pais == "all" devuelve todos los paises

    Parameters
    ----------
    datos_poblacion: dict
        Diccionario con los datos de poblacion 
    fecha_ini, fecha_fin : int
        Fecha de inicio y fin del intervalo
    pais: str, optional
        Nombre del pais a consultar. Default: "all"

    Returns
    -------
    pandas.DataFrame
        Tabla, en formato DataFrame, con los valores de poblacion
        
    Precondition
    ------------
    fecha_ini <= fecha_fin
        La fecha de inicio debe ser menor o igual a la fecha de fin
    
    Example
    -------
    >> generar_tabla_poblacion(datos_poblacion, 1998, 1999)
              Afghanistan Albania  Algeria
    1998       101976989  11876991 12001002
    1999        8976981   91976989 101976989
    ...
    """
    if fecha_ini > fecha_fin:
        raise ValueError("Error. La fecha de fin debe ser mayor a la fecha de inicio")

    rango_fechas = set(range(fecha_ini, fecha_fin+1))

    if pais == "all":
        diccionario_datos = apartado_b.obtener_poblacion_paises_annos(datos_poblacion, set(datos_poblacion.keys()) , rango_fechas)
    else:
        diccionario_datos = apartado_b.obtener_poblacion_paises_annos(datos_poblacion, {pais}, rango_fechas)

    return pd.DataFrame.from_dict(diccionario_datos).sort_index(axis=1)