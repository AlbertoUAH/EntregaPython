"""
@author: alberto
"""

# apartado e)
import pandas as pd
import re
import os

def causas_fallecimiento(fichero):
    """
    Funcion que recupera la tabla con los datos de las causas de fallecimiento
    por cada pais y anno, en formato DataFrame. Las columnas del DataFrame, 
    por su parte, son renombradas (en caso de incluir nombres con '-')
    
    Parameters
    ----------
    fichero : str
        Nombre del fichero

    Returns
    -------
    pandas.DataFrame
        Tabla con los datos extraidos del csv
        
    Preconditions
    -------------
    El fichero:
        debe estar situado en la ruta indicada
        NO debe estar vacio
        debe estar en formato .csv
    
    Example
    -------
    >>> causas_fallecimiento('annual-number-of-deaths-by-cause.csv')
             Entity  Year   ... - Interpersonal violence -
    5561     Spain   1991   ...         447.616375
    5562     Spain   1992   ...         428.134996
    """
    if not os.path.exists(fichero):
        raise FileNotFoundError("Error. El fichero no se encuentra en el directorio actual")

    elif os.stat(fichero).st_size == 0:
        raise StopIteration("Error. El fichero esta vacio")

    elif not fichero.endswith(".csv"):
        raise Exception("Error. El fichero debe estar en formato csv")

    df_mortalidad = pd.read_csv(fichero)

    lista_columnas = df_mortalidad.columns.values.tolist()
    df_mortalidad.columns = renombrar_columnas(lista_columnas)

    return df_mortalidad.fillna(0)
	
def renombrar_columnas(columnas):
    """
    Funcion encargada de renombrar las columnas, empleando una
    expresion regular que simplifica el nombre de cada columna entre
    guiones
    
    Parameters
    ----------
    columnas : list
        Lista con los nombres originales de columnas

    Returns
    -------
    list
        Lista con el nombre de cada columna simplificado
    
    Example
    -------
    >>> renombrar_columnas([-Deaths - Road injuries - Sex: Both - Age: All Ages (Number)-])
    [- Road injuries -]
    """

    patron = re.compile("- (.*?) -")
    return list(map(lambda columna : re.search(patron, columna)[0].strip() if '-' in columna else columna, columnas))
	
def filtrar_tabla(df_fallecimientos, nombre_columna, filtro):
    """
    Metodo que permite filtrar los valores del DataFrame en funcion 
    de la columna proporcionada y el conjunto de parametros.
    AVISO: en caso de NO coincidir ningun elemento del DataFrame 
    con el/los parametros, devuelve una tabla vacia

    Parameters
    ----------
    df_fallecimientos : pandas.DataFrame
        Tabla de datos con el numero de fallecimientos
    nombre_columna : str
        Nombre de la columna sobre la que aplicar el filtro
    filtro : set
        Conjunto de valores a seleccionar

    Returns
    -------
    pandas.DataFrame
        Tabla con los valores filtrados
        
    Precondition
    ------------
    El DataFrame inicial NO debe estar vacio
    El campo nombre_columna debe estar en el DataFrame, asi como
    los valores del filtro
    El campo "filtro" NO debe estar vacio ({})

    Example
    -------
    >>> filtrar_tabla(df_fallecimientos, "Year", {1998, 1999})
           Entity  Year   ... - Interpersonal violence -
    1      Spain   1998   ...         447.616375
    2      Spain   1999   ...         428.134996 
    3      Italy   1998   ...         217.326058
    4      Italy   1999   ...         178.134986 
    """
    if df_fallecimientos.empty:
        raise ValueError("Error. El DataFrame esta vacio")
    elif nombre_columna not in df_fallecimientos.columns:
        raise KeyError("Error. No se ha encontrado el nombre de la columna \'" + nombre_columna + "\'")
    elif filtro == {}:
        raise ValueError("Error. El campo filtro esta vacio ({})")
    
    df_fallecimientos_filtrado = df_fallecimientos[df_fallecimientos[nombre_columna].isin(filtro)]
    if df_fallecimientos_filtrado.empty:
        raise ValueError("Error. No se han encontrado filas para los valores: " + str(filtro))

    return df_fallecimientos_filtrado
	
def eliminar_caracter(columna, caracter):
    """
    Funcion que elimina un caracter de una columna, en formato de expresion 
    regular, y su posterior conversion a formato float

    Parameters
    ----------
    columna : pandas.Series
        Columna sobre la que aplicar la funcion
    caracter : str
        Expresion regular con la que sustituir una cadena de caracteres

    Returns
    -------
    pandas.Series
        Columna con los valores convertidos a formato float
    """    
    if any(columna.astype(str).str.contains(caracter, na = False)) == True:
        return columna.replace(caracter, '', regex=True).astype(float)
    else:
        return columna

