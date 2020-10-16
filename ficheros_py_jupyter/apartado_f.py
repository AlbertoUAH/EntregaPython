"""
@author: alberto
"""
# apartado f)
import pandas as pd
import apartado_b
import apartado_e

ENTITY = "Entity"; YEAR = "Year"

def calcular_tasa_fallecimiento(df_fallecimientos, datos_poblacion, param_pais, param_anno, param_causa, tasa):
    """
    Funcion que calcula la tasa de mortalidad por numero de habitantes, pais y anno

    Parameters
    ----------
    df_fallecimientos : pandas.DataFrame
        Tabla de datos con los valores de mortalidad de diferentes paises y annos
    datos_poblacion : dict
        Diccionario con los valores de poblacion en cada pais y anno
    param_pais, param_anno, param_causa : str
        Pais, anno y causa de fallecimiento, respectivamente
    tasa: int
        Tasa de habitantes

    Returns
    -------
    float
        Tasa de fallecimiento resultante (redondeada a 2 decimales)
    
    Preconditions
    -------------
    Los parametros de consulta (pais, anno, causa fallecimiento)
    deben existir en el DataFrame
    Los valores contenidos en la columna param_causa DEBEN ser numericos
    La tasa debe ser estrictamente mayor que 0 (tasa > 0)
    
    Example
    -------
    >>> calcular_tasa_mortalidad(df_fallecimientos, datos_poblacion, "Spain", 2015, "- Road injuries -", 10000)
    0.54
    """
    try:
        poblacion = apartado_b.obtener_poblacion_paises_annos(datos_poblacion, {param_pais}, {param_anno})

        df_causas_fallecimiento = pd.merge(apartado_e.filtrar_tabla(df_fallecimientos, ENTITY, {param_pais}),\
                                           apartado_e.filtrar_tabla(df_fallecimientos, YEAR, {param_anno}), how = "inner")

        if param_causa not in df_causas_fallecimiento.columns:
            raise KeyError("Error. La causa de mortalidad \'" + param_causa + "\' no existe como columna")
        elif tasa <= 0:
            raise AttributeError("Error. La tasa debe ser estrictamente mayor que 0")
    
        tasa_fallecimiento = (df_causas_fallecimiento[param_causa][0] / poblacion[param_pais][param_anno]) * tasa
        return round(tasa_fallecimiento, 2)
    except TypeError as e:
        print("Error. La tasa de mortalidad se ha intentado calcular con valores NO numericos")