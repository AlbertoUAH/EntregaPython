"""
@author: alberto
"""
# apartado g)
from matplotlib import rc
import matplotlib.pyplot as plt
import pandas as pd
import apartado_f

def comparar_mortalidad(df_fallecimientos, datos_poblacion, param_paises, param_anno, param_causa, tasa):
    """
    Funcion que devuelve un grafico comparativo de la mortalidad
    por una causa en un anno, dada una coleccion de paises

    Parameters
    ----------
    df_fallecimientos : pandas.DataFrame
        Tabla de datos con los valores de mortalidad de diferentes paises y annos
    param_paises : set
        Conjunto con los nombres de los paises a comparar
    param_anno : int
        Anno a filtrar en datos_fallecimientos
    param_causa : str
        Causa de mortalidad con la que comparar
    tasa : int
        Tasa de habitantes

    Returns
    -------
    ax : Figure
        Grafico de barras final, mostrando los valores de mortalidad de cada pais,
        en un anno y causa en particular
    """
    tasas_mortalidad = [[pais, apartado_f.calcular_tasa_fallecimiento(df_fallecimientos, datos_poblacion, pais, param_anno, param_causa, tasa)] for pais in param_paises]

    df_tasas_mortalidad = pd.DataFrame(tasas_mortalidad, columns = [ENTITY, param_causa])
    df_tasas_mortalidad = df_tasas_mortalidad.sort_values(param_causa)
    grafico_barras = imprimir_grafico_barras(df_tasas_mortalidad[ENTITY], df_tasas_mortalidad[param_causa], 'mediumpurple')

    for indice, valor in enumerate(df_tasas_mortalidad[param_causa]):
        plt.text(valor, indice, valor, verticalalignment='center', fontsize = 10)

    plt.title("Mortalidad " + param_causa + " (por cada " + str(tasa) + " hab.)")
    plt.ylabel("Paises", fontsize=12)
    plt.xlabel("Tasa de mortalidad", fontsize=12)

    return plt.show()

def imprimir_grafico_barras(y, x, color):
    """
    Funcion auxiliar que devuelve la grafica de ambas tablas
    
    Parameters
    ----------
    x : pandas.Series
        Tabla de datos con las coordenadas del eje X
    y : pandas.Series / pandas.Index
        Tabla de datos (e incluso un indice) con las coordenadas del eje Y
    color : str
        Color del grafico    

    Returns
    -------
    Figure
        Grafico de barras final (en horizontal)
    """       
    rc("font", weight = "bold")
    figura  = plt.figure(figsize=(10,10))
    
    plt.barh(y, x, height = 0.6, color = color)
    plt.yticks(y)
    
    plt.ticklabel_format(axis = 'x', useOffset=False)
    plt.autoscale() 
    plt.rcParams["axes.labelweight"] = "bold"
    plt.style.use("ggplot")
    
    return figura