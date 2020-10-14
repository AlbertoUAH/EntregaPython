# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 16:09:49 2020

@author: alberto
"""
#apartado h)
import os
import apartado_e

def eliminar_filas(datos_fallecimientos, columna, fichero):
    """
    Funcion encargada de eliminar aquellas filas del DataFrame
    en funcion de los valores de la columna indicada, filtrando
    aquellos que no esten contenidos en el fichero

    Parameters
    ----------
    datos_fallecimientos : pandas.DataFrame
        DataFrame con los valores de mortalidad
        en los distintos paises y annos
    columna : str
        Nombre de la columna
    fichero : str
        Ruta del fichero de texto con el que aplicar el filtro

    Returns
    -------
    pandas.DataFrame
        DataFrame con los valores filtrados
        
    Precondition
    ------------
    El fichero debe estar situado en la ruta
    indicada por parametro
    
    El fichero debe estar en formato .txt
    
    La columna indicada debe estar contenida en el DataFrame
    """
    if not os.path.exists(fichero):
        raise FileNotFoundError("Error. El fichero no se encuentra en el directorio actual")
        
    elif not fichero.endswith('.txt'):
        raise Exception("Error. El fichero debe estar en formato txt")
    
    elif columna not in datos_fallecimientos.columns:
        raise KeyError("Error. La columna indicada no forma parte del DataFrame")
    
    with open(fichero, "r") as f:
        conjunto_paises = {pais.rstrip('\n') for pais in f.readlines()}

    return datos_fallecimientos[~datos_fallecimientos[columna].isin(conjunto_paises)]

def eliminar_ceros(datos_fallecimientos, columnas):
    """
    Funcion que permite eliminar aquellas filas
    cuyos valores contenidos en las columnas sean ceros

    Parameters
    ----------
    datos_fallecimientos : pandas.DataFrame
        DataFrame con los valores de mortalidad
        en los distintos paises y annos
    columnas : set
        Conjunto de columnas sobres las que aplicar el filtro

    Returns
    -------
    pandas.DataFrame
        DataFrame con las filas a ceros eliminadas
    
    Precondition
    ------------
    El DataFrame NO debe estar vacio
    
    El conjunto de columnas debe existir en el DataFrame
    """
    if datos_fallecimientos.empty:
        raise ValueError("Error. El DataFrame esta vacio")
    
    elif not columnas.issubset(datos_fallecimientos.columns):
        raise KeyError("Error. El conjunto de columna/s no forma/n parte del DataFrame")
    
    return datos_fallecimientos[~(datos_fallecimientos.loc[:, columnas] == 0).all(axis = 1)]

def suma_causas_fallecimientos(datos_fallecimientos, param_anno, columnas):
    """
    Funcion que calcula el total de fallecimientos en un anno dado por
    cada causa

    Parameters
    ----------
    datos_fallecimientos: pandas.DataFrame
        DataFrame con los valores de mortalidad
        en los distintos paises y annos
    param_anno : int
        Anno a consultar
    columnas : set
        Conjunto de columnas con las causas
        de fallecimiento a calcular

    Returns
    -------
    dict
        Diccionario con la suma acumulada
        de cada causa de fallecimiento
    
    Preconditions
    -------------
    En caso de no encontrar ninguna coincidencia con el anno, 
    devolvera un error, indicando que no se disponen de datos
    
    El listado de columnas deben estar incluidas en el DataFrame
    
    Las columnas deben contener valores numericos
    
    Example
    -------
    >>> suma_causas_fallecimientos(datos_fallecimientos, 2017, {'- Road injuries -', '- Tuberculosis -'})
    {
        '- Road injuries -': 5785093,
        '- Tuberculosis -': 5388766
    }
    """
    
    df_causas_fallecimientos = apartado_e.filtrar_tabla(datos_fallecimientos, 'Year', {param_anno})
    
    if df_causas_fallecimientos.empty:
        raise ValueError("Error. No de disponen de datos para dicho anno en particular")
    
    elif not columnas.issubset(df_causas_fallecimientos.columns):
        raise KeyError("Error. El conjunto de columna/s no forma/n parte del DataFrame")
    
    try:
        causa_fallecimientos = dict()
        
        for _, fila in df_causas_fallecimientos.iterrows():
            for columna in columnas:
                if columna not in causa_fallecimientos.keys():
                    causa_fallecimientos[columna] = round(fila[columna],2)
                else:
                    causa_fallecimientos[columna] += round(fila[columna],2)
        return causa_fallecimientos
    
    except TypeError as e:
        print("Error. El DataFrame contiene valores NO numericos")
        raise(e)