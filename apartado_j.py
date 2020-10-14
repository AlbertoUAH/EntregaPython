# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 15:44:58 2020

@author: alberto
"""
# apartado j)
from matplotlib import cm
from matplotlib import rc
import matplotlib.pyplot as plt
import pandas as pd
import re
import apartado_e

def generar_grafica(datos_fallecimientos, param_pais, param_anno, escala = "linear"):
    """
    Funcion que permite, mediante varias funciones sucesivas,filtra una parte 
    de la tabla de datos (En funcion del pais y anno) y su representacion 
    grafica en funcion de una escala determinada

    Parameters
    ----------
    datos_fallecimientos : pandas.DataFrame
        DataFrame con los datos de fallecimientos por pais, anno y causa
    param_pais : str
        Nombre del pais a consultar
    param_anno : int
        Anno de consulta
    escala : str
        Escala de representacion (optional)
        Por defecto: linear

    Returns
    -------
    Figure
        Grafico de barras con la comparativa entre
        las diferentes causas de mortalidad en el
        pais y anno de consulta
    pandas.DataFrame
        DataFrame con los valores de la tabla filtrados
        por pais y anno de consulta

    Precondition
    ------------
    En caso de no encontrar datos para el pais y anno
    de consulta, devolvera un error, indicando que no
    se disponen de valores
    
    La escala solo puede ser linear (linear) o logaritmica (log)
    """

    for columna in datos_fallecimientos.columns:
        datos_fallecimientos[columna] = apartado_e.eliminar_caracter(datos_fallecimientos[columna],'[>]+')
    
    df_causas_fallecimiento = pd.merge(apartado_e.filtrar_tabla(datos_fallecimientos, 'Entity', param_pais),\
                                           apartado_e.filtrar_tabla(datos_fallecimientos, 'Year', {param_anno}), how = 'inner')
        
    if df_causas_fallecimiento.empty:
        raise ValueError("Error. No de disponen de datos para el/los pais/es y/o anno en particular") 
    
    if escala not in ["linear", "log"]:
        raise ValueError("Error. La escala solo puede ser lineal (lineal) o logaritimica (log")
    
    return imprimir_grafica(df_causas_fallecimiento, param_pais, param_anno, escala), df_causas_fallecimiento


def imprimir_grafica(df_causas_fallecimiento, param_pais, param_anno, escala):
    """
    Funcion que crea un grafico de barras a partir del DataFrame pasado
    como parametro, concretamente un grafico de barras en horizontal en
    una escala pasada como parametro

    Parameters
    ----------
    df_causas_fallecimiento : pandas.DataFrame
        DataFrame con los valores de mortalidad del pais y anno
    param_pais : str
        Nombre del pais a consultar
    param_anno : int
        Anno de consulta
    escala: str
        Escala de representacion

    Returns
    -------
    ax : Figure
        Grafico de barras final, comparando los valores de mortalidad de
        cada causa

    """
    df_causas_fallecimiento.columns = limpiar_nombres_columnas(df_causas_fallecimiento.columns)
    
    traspuesta = df_causas_fallecimiento.iloc[:,3:].T.sort_values(0)
    traspuesta = traspuesta.rename(columns = {0: "numero_fallecimientos"})
    
    lista_colores = cm.get_cmap("viridis", len(traspuesta))

    rc('font', weight = 'bold')
    figura, ax = plt.subplots()
    
    ax.barh(traspuesta.index, traspuesta["numero_fallecimientos"], color = lista_colores.colors[::-1])
    ax.set_title("Comparativa valores mortalidad. Pais: " + param_pais + ". Año: " + str(param_anno), fontweight='bold')
    ax.set_xlabel("Total fallecimientos", fontweight='bold')
    ax.set_xscale(escala)
    
    xlabels = [formatear_numero(numero) for numero in ax.get_xticks()]
    ax.set_xticklabels(xlabels)
    ax.grid(axis='x', linestyle = '--')
    
    for indice, valor in enumerate(traspuesta["numero_fallecimientos"]):
        ax.text(valor, indice, formatear_numero(valor), verticalalignment='center', fontsize = 7)
        
    plt.annotate('Fuente: https://ourworldindata.org', (0,0), (-80,-30), fontsize=8, xycoords='axes fraction', textcoords='offset points')
    plt.yticks(fontsize = 7)
    plt.rcParams['axes.labelweight'] = 'bold'
    plt.show()
    return ax

def formatear_numero(numero):
    """
    Funcion que permite dar formato a un numero
    para su representacion grafica.
    Ejemplo:
        2145987 -> 2.14 Mill
        365786 -> 365,786

    Parameters
    ----------
    numero : int
        Numero a formatear

    Returns
    -------
    str
        Numero con el formato especifico
        (en funcion de si es del orden de millones o no)

    """
    if numero >= 10**6:
        return str(round(numero / 10**6, 2)) + " Mill."
    else:
        return format(round(numero), ",")

def limpiar_nombres_columnas(nombres_columnas):
    """
    Funcion que permite "limpiar" caracteres de
    las columnas de un DataFrame, concretamente
    los valores entre parentesis, palabras como
    and, other, of, exposure, disease/s, guiones,
    asi como espacios en blanco adicionales

    Parameters
    ----------
    nombres_columnas : set
        Conjunto con los nombres de columnas

    Returns
    -------
    list
        Listado con los nombres de columnas
        procesados
    """
    caracteres = [re.compile("\(.*\)"), re.compile("(and|other|of|exposure|disease(s)?|-)"), re.compile(" +")]
    
    for caracter in caracteres:
        nombres_columnas = list(map(lambda columna : re.sub(caracter, ' ', columna), nombres_columnas))
    
    return [columna.strip().capitalize() for columna in nombres_columnas]

generar_grafica('annual-number-of-deaths-by-cause.csv', 'China', 2015, 'linear')