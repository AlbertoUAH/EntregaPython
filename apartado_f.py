#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 20:55:58 2020

@author: alberto
"""
# Apartado f)
import pandas as pd
import apartado_b
import apartado_e

def calcular_tasa_fallecimiento(datos_fallecimientos, datos_poblacion, param_pais, param_anno, param_causa, tasa):
    """
    Funcion que calcula, para una causa de muerte en un pais y anno en 
    concreto, la tasa de muerte por cada numero de habitantes indicado por
    el parametro tasa

    Parameters
    ----------
    datos_fallecimientos : pandas.DataFrame
        Tabla de datos con los valores
        de mortalidad de diferentes paises y
        annos
    datos_poblacion : dict
        Diccionario con los valores de poblacion
        en cada pais y anno
    param_pais : str
        Nombre del pais a consultar
    param_anno : str
        Anno a consultar
    param_causa : str
        Causa de fallecimiento
        con la que calcular la tasa
    tasa: int
        Tasa de habitantes

    Returns
    -------
    float
        Tasa de fallecimiento resultante por cada 10000 habitantes 
        (aproximada a dos cifras decimales)
    
    Preconditions
    -------------
    Los parametros de consulta (pais, anno, causa fallecimiento)
    deben existir , de lo contrario devolvera un error indicando
    que no se disponen de datos para el pais/anno/causa en particular/es
    
    Los valores contenidos en la columna param_causa DEBEN ser numericos
    
    La tasa de habitantes debe ser estrictamente mayor que 0
    
    Example
    -------
    >>> calcular_tasa_mortalidad(fichero, fichero_poblacion, "Spain", 2015, "- Road injuries -", 10000)
    0.54
    """
    poblacion = apartado_b.obtener_poblacion_paises_annos(datos_poblacion, {param_pais}, {param_anno})
    df_causas_fallecimiento = pd.merge(apartado_e.filtrar_tabla(datos_fallecimientos, 'Entity', {param_pais}),\
                                       apartado_e.filtrar_tabla(datos_fallecimientos, 'Year', {param_anno}), how = 'inner')
        
    if poblacion == {} or df_causas_fallecimiento.empty:
        raise ValueError("Error. No de disponen de datos para el pais y anno en particular")
    elif param_causa not in df_causas_fallecimiento.columns:
        raise KeyError("Error. La causa de mortalidad no existe como columna")
    elif tasa <= 0:
        raise AttributeError("Error. La tasa debe ser estrictamente mayor que 0")
    
    try:
        return round(((df_causas_fallecimiento[param_causa][0]) / poblacion[param_pais][param_anno]) * tasa, 2)
    except TypeError as e:
        print("Error. La tasa de mortalidad se ha intentado calcular con valores NO numericos")
        raise(e)