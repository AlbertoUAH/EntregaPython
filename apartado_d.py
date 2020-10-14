#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 07:52:49 2020

@author: alberto
"""
# Apartado d)
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

def mostrar_comparacion(df_evolucion_poblacion_pais, df_evolucion_poblacion_mundial):
    """
    Funcion encargada de mostrar graficamente la comparacion entre los valores 
    de poblacion mundial y los valores re-escalados de un pais

    Parameters
    ----------
    df_evolucion_poblacion_pais: pandas.DataFrame
        DataFrame con los datos a comparar
    df_evolucion_poblacion_mundial : pandas.DataFrame
        DataFrame con los datos de la poblacion mundial

    Returns
    -------
    Figure
        Grafica comparativa entre los valores
        del pais seleccionado y la poblacion
        mundial

    Precondition
    ------------
    Ambos DataFrames NO deben estar vacios
    
    Ambos DataFrames deben contener valores numericos
    """
    if df_evolucion_poblacion_mundial.empty or df_evolucion_poblacion_pais.empty:
        raise ValueError("Error. La/s tabla/s esta/n vacia/s")
        
    try:
        pobl_min_pais, pobl_max_pais = obtener_valores_min_max(df_evolucion_poblacion_pais)
        pobl_min_glob, pobl_max_glob = obtener_valores_min_max(df_evolucion_poblacion_mundial)
        formula_escalado = lambda poblacion: ((poblacion - pobl_min_pais) / (pobl_max_pais - pobl_min_pais)) * (pobl_max_glob - pobl_min_glob) + pobl_min_glob
        
        return imprimir_grafica(df_evolucion_poblacion_mundial, df_evolucion_poblacion_pais.apply(formula_escalado))
    except TypeError:
        print("Error. El DataFrame contiene valores NO numericos")
# URL: https://stats.stackexchange.com/questions/281162/scale-a-number-between-a-range

def obtener_valores_min_max(df_evolucion_poblacion):
    """
    Funcion axiliar que extrae los valores minimo y maximo
    del DataFrame dado como parametro

    Parameters
    ----------
    df_evolucion_poblacion : pandas.DataFrame
        DataFrame del que extraer los valores
        minimo y maximo

    Returns
    -------
    int, int
        Tupla con los valores maximo y minimo.
    
    Example
    -------
    >>> obtener_valores_min_max(pd.DataFrame({"A":[12,45,23]}))
    12,23
    """
    return int(df_evolucion_poblacion.min()), int(df_evolucion_poblacion.max())


def imprimir_grafica(df_evolucion_poblacion_mundial, df_evolucion_poblacion_pais):
    """
    Funcion que imprime un grafico
    comparativo entre ambos DataFrames

    Parameters
    ----------
    df_evolucion_poblacion_mundial : DataFrame
        DataFrame con los datos de la poblacion mundial
    df_evolucion_poblacion_pais : DataFrame
        DataFrame con los datos de la poblacion de un pais

    Returns
    -------
    ax : Figure
        Grafica comparativa con los datos de
        ambos DataFrames

    """
    pais = list(df_evolucion_poblacion_pais.columns)
    
    figura, (ax1, ax2) = plt.subplots(2, figsize = (12,12))
    
    plt.ticklabel_format(useOffset=False)
    ax1.plot(df_evolucion_poblacion_mundial, c="blue", linewidth=2.0)
    ax2.plot(df_evolucion_poblacion_pais, c="orange", linewidth=2.0)
    
    ax1.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax2.xaxis.set_major_locator(MaxNLocator(integer=True))
    
    ax2.set_xlabel("Años", fontsize=15)
    ax1.set_ylabel("Total poblacion", fontsize=15)
    ax2.set_ylabel("Total poblacion (re-escalado)", fontsize=15)
    
    ax1.legend(["Evolucion poblacion mundial"], loc="best")
    ax2.legend(["Evolucion poblacion -pais: " + pais[0] + "-"], loc="best")
    
    plt.style.use('ggplot')
    plt.autoscale() 
    
    return ax1, ax2