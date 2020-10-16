"""
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
        DataFrame con los valores de mortalidad en los distintos paises y annos
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
    El fichero:
               debe estar situado en la ruta indicada por parametro
               debe estar en formato .txt
    La columna indicada debe estar contenida en el DataFrame
    """
    if not os.path.exists(fichero):
        raise FileNotFoundError("Error. El fichero no se encuentra en el directorio actual")
        
    elif not fichero.endswith(".txt"):
        raise Exception("Error. El fichero debe estar en formato txt")
    
    elif columna not in df_fallecimientos.columns:
        raise KeyError("Error. La columna \'" + columna + "\' no forma parte del DataFrame")
    
    with open(fichero, "r") as f:
        regiones = {pais.rstrip('\n') for pais in f.readlines()}

    filtro = set(df_fallecimientos[columna].values) - regiones
    return filtrar_tabla(df_fallecimientos, columna, filtro)

def suma_causas_fallecimientos(df_fallecimientos, param_anno, columnas):
    """
    Funcion que calcula el total de fallecimientos en un anno en las columnas dadas

    Parameters
    ----------
    df_fallecimientos: pandas.DataFrame
        DataFrame con los valores de mortalidad en los distintos paises y annos
    param_anno : int
        Anno a consultar
    columnas : set
        Conjunto de columnas con las causas de fallecimiento a calcular

    Returns
    -------
    dict
        Diccionario con la suma acumulada de cada causa de fallecimiento
    
    Preconditions
    -------------
    Las columnas:
                 deben estar incluidas en el DataFrame
                 deben contener valores numericos
    
    Example
    -------
    >>> suma_causas_fallecimientos(df_fallecimientos, 2015, {'- Poisonings -'})
    {
        '- Poisonings -': 73894
    }
    """
    df_filtrado = apartado_e.filtrar_tabla(df_fallecimientos, YEAR, {param_anno})
    
    if not columnas.issubset(df_filtrado.columns):
        columnas_sobrantes = columnas - set(df_filtrado.columns)
        raise KeyError("Error. El conjunto " + str(columnas_sobrantes) + " no son columnas del DataFrame")
    
    try:
        causa_fallecimientos = dict()
        
        for _, fila in df_filtrado.iterrows():
            for columna in sorted(columnas):
                if columna not in causa_fallecimientos.keys():
                    causa_fallecimientos[columna] = round(fila[columna])
                else:
                    causa_fallecimientos[columna] += round(fila[columna])
        return causa_fallecimientos
    
    except TypeError as e:
        print("Error. El DataFrame contiene valores NO numericos")