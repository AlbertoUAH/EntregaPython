#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 07:48:47 2020

@author: alberto
"""
import apartado_b
import pandas as pd

# Apartado c)
def generar_tabla_poblacion(datos_poblacion, pais, fecha_ini, fecha_fin):
    """
    Funcion que permite generar una tabla, en formato DataFrame, con 
    las poblaciones del pais pasados como parametro, entre dos annos.
    AVISO: Si un anno no  se encuentra registrado para un pais, 
    devuelve NaN para dicho campo.
    Si pais == "all" devuelve todos los paises

    Parameters
    ----------
    datos_poblacion: dict
        Diccionario con los datos
        a convertir  
    pais: str
        Nombre del pais a consultar
    fecha_ini : int
        Fecha de inicio del intervalo
    fecha_fin : int
        Fecha de fin del intervalo

    Returns
    -------
    pandas.DataFrame
        Tabla, en formato DataFrame, con los valores
        de poblacion
        
    Precondition
    ------------
    fecha_ini < fecha_fin
        La fecha de inicio debe ser menor a la fecha de fin
    
    Example
    -------
    >> generar_tabla_poblacion(1998, 2000)
                    1998     1999     2000
    Afghanistan  101976989  11876991 12001002
    Albania       8976981   91976989 101976989
    ...
    """
    assert type(datos_poblacion) is dict and type(pais) is str \
        and type(fecha_ini) is int and type(fecha_fin) is int, \
        "Error, parametros no validos: generar_tabla_poblacion(dict, str, int, int)"
    
    if fecha_ini > fecha_fin:
        raise ValueError("Error. La fecha de fin debe ser mayor a la fecha de inicio")
        
    rango_fechas = set(range(fecha_ini, fecha_fin+1))
    
    if pais == "all":
        diccionario_datos = apartado_b.obtener_poblacion_annos(datos_poblacion, rango_fechas)
    else:
        diccionario_datos = apartado_b.obtener_poblacion_paises_annos(datos_poblacion, {pais}, rango_fechas)
    
    return pd.DataFrame.from_dict(diccionario_datos).sort_index(axis=1)