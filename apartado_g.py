#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 10:40:01 2020

@author: alberto
"""
# Apartado g)
from matplotlib import rc
import matplotlib.pyplot as plt
import pandas as pd
import apartado_f



def comparar_mortalidad(datos_fallecimientos, datos_poblacion, param_paises, param_anno, param_causa, tasa):
    """
    Funcion que devuelve un grafico comparativo de la mortalidad
    por una causa en un anno, dada una coleccion de paises

    Parameters
    ----------
    datos_fallecimientos : pandas.DataFrame
        Tabla de datos con los valores
        de mortalidad de diferentes paises y
        annos
    param_paises : set(str)
        Conjunto con los nombres
        de los paises a comparar
    param_anno : int
        Anno a filtrar en datos_fallecimientos
    param_causa : str
        Causa de mortalidad con la que comparar
    tasa : int
        Tasa de habitantes

    Returns
    -------
    ax : Figure
        Grafico de barras final, mostrando
        los valores de mortalidad de cada pais,
        en un anno y causa en particular
        
    Preconditions
    -------------
    Los paises a comparar deben estar (TODOS) en el DataFrame pasado como
    parametro
    
    Los valores contenidos en la columna param_causa DEBEN SER NUMERICOS
    """
    df_mortalidad = pd.DataFrame(columns = ['Entity', param_causa])
    
    for pais in param_paises:
        tasa_mortalidad = apartado_f.calcular_tasa_fallecimiento(datos_fallecimientos, datos_poblacion, pais, param_anno, param_causa, tasa)
        df_mortalidad.loc[len(df_mortalidad),:] = [pais , tasa_mortalidad]

    if df_mortalidad.empty:
        raise ValueError("Error. No de disponen de datos para el/los pais/es y/o anno en particular")
        
    elif param_causa not in df_mortalidad.columns:
        raise KeyError("Error. La causa de mortalidad no existe como columna")
    
    df_mortalidad = df_mortalidad.sort_values(param_causa)
        
    return imprimir_grafico_barras(df_mortalidad, param_causa, tasa)

def imprimir_grafico_barras(df_causas_fallecimiento, param_causa, tasa):
    """
    Funcion auxiliar que devuelve la grafica
    de ambas tablas
    
    Parameters
    ----------
    df_causas_fallecimiento : pandas.DataFrame
        Tabla de datos con las causas de
        fallecimiento en un conjunto de paises,
        en un anno concreto
    param_causa : str
        Causa de mortalidad
    tasa : int
        Tasa de habitantes    

    Returns
    -------
    ax : Figure
        Grafico de barras final, mostrando
        la mortalidad de cada pais
    """       
    rc('font', weight = 'bold')
    figura, ax = plt.subplots()
    ax.barh(df_causas_fallecimiento['Entity'], df_causas_fallecimiento[param_causa], color = 'mediumpurple')
    
    ax.set_title(param_causa + " (por cada " + str(tasa) + " hab.)")
    ax.set_ylabel("Paises", fontsize=10)
    ax.set_xlabel("Tasa de mortalidad", fontsize=10)
    
    plt.yticks(df_causas_fallecimiento['Entity'])
    plt.autoscale() 
    plt.rcParams['axes.labelweight'] = 'bold'
    plt.style.use('ggplot')
    return ax