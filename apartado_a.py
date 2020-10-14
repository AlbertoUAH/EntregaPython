#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 15:20:09 2020

@author: alberto
"""

# Apartado a)
import csv
import os

def crecimiento_por_pais(filas):
    """
    Funcion auxiliar que devuelve un diccionario con las parejas anno, 
    poblacion (clave, valor) de un pais
    
    Parameters
    ----------
    filas: list
        Lista de listas con el total de poblacion en
        cada anno de un pais
    
    Return
    ------
    dict
        Diccionario formado por las parejas
        anno (clave) y poblacion (valor),
        ambos valores enteros
        
    Example
    -------
    >>> crecimiento_por_pais([1900, 20134543], [1901, 20554593])
    {
        1900:20134543,
        1901:20554593
    }      
    """
    return {int(fila[0]) : int(fila[1]) for fila in filas}

def crecimiento_por_pais_anno(fichero):
    """
    Funcion que devuelve un diccionario que contiene el valor de poblacion por 
    cada pais y anno almacenado en el fichero, SALVO el campo Code, situado
    en la segunda columna
    
    Parameters
    ----------
    fichero: str
        Nombre del fichero a recuperar
    
    Return
    ------
    dict
        Diccionario formado por las parejas pais (clave) y, como valor, 
        un diccionario con la poblacion en cada anno
    
    Precondition
    ------------
    El fichero:
        Debe estar situado en la ruta indicada por parametro
    
        Debe estar en formato .csv
    
        NO debe estar vacio
    
        Debe tener como MINIMO tres columnas
        
    Example
    -------
    >>> crecimiento_por_pais_anno('population.csv')
    {
        "Spain": {
            1900:20134543,
            1901:20554593,
            1902:20994983
        },
        "France": {
            1900:20934543,
            1901:21050194,
            1902:21764183
        }
        ...
    }      
    """
    if not os.path.exists(fichero):
        raise FileNotFoundError("Error. El fichero no se encuentra en el directorio actual")
        
    elif not fichero.endswith('.csv'):
        raise Exception("Error. El fichero debe estar en formato csv")
    
    elif os.stat(fichero).st_size == 0:
        raise StopIteration("Error. El fichero esta vacio")
    
    with open(fichero) as archivo:
        archivo_csv = csv.reader(archivo, delimiter=",")
            
        next(archivo_csv)
        filas = [fila for fila in archivo_csv]
        
        if len(filas) < 3:
            raise IndexError("Error. El fichero debe tener como minimo tres columnas")
        
        paises = sorted(set(fila[0] for fila in filas))
        [fila.pop(1) for fila in filas]

        crecimiento_annos = {pais: crecimiento_por_pais([fila[1:] for fila in filas if pais in fila]) for pais in paises}
    return crecimiento_annos