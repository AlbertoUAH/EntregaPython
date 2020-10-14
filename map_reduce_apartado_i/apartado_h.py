# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 16:09:49 2020

@author: alberto
"""
#apartado h)
import os
import apartado_e

def eliminar_filas(df_fallecimientos, columna, fichero):
    """
    Funcion encargada de eliminar aquellas filas del DataFrame en funcion de los 
    valores de la columna indicada, eliminando aquellos que esten contenidos en el fichero

    Parameters
    ----------
    df_fallecimientos : pandas.DataFrame
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
    El fichero debe estar situado en la ruta indicada por parametro
    El fichero debe estar en formato .txt
    La columna indicada debe estar contenida en el DataFrame
    """
    if not os.path.exists(fichero):
        raise FileNotFoundError("Error. El fichero no se encuentra en el directorio actual")
        
    elif not fichero.endswith('.txt'):
        raise Exception("Error. El fichero debe estar en formato txt")
    
    elif columna not in df_fallecimientos.columns:
        raise KeyError("Error. La columna indicada no forma parte del DataFrame")
    
    with open(fichero, "r") as f:
        regiones = {pais.rstrip('\n') for pais in f.readlines()}

    filtro = set(df_fallecimientos[columna].values) - regiones
    return apartado_e.filtrar_tabla(df_fallecimientos, columna, filtro)