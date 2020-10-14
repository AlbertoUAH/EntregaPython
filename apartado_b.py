#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 19:08:31 2020

@author: alberto
"""
# Apartado b)
def obtener_poblacion_paises(datos_poblacion, param_paises):
   """
   Funcion auxiliar que recupera los valores de poblacion,
   para todos los annos, en el/los pais/es dado/s
   
   Parameters
   ----------
   datos_poblacion : dict
        Fichero con los datos de la poblacion mundial
   param_paises : set(str)
        Nombre/s del pais/es a consultar
    
   Returns
   -------
   dict
       Diccionario con los datos de poblacion
       en el/los pais/es pasado/s como argumento/s
       AVISO: Si NO encuentra resultados, devuelve un diccionario
       vacio ({})
    
   Precondition
   ------------
   El diccionario pasado como parametro NO debe estar vacio, asi como
   tambien sus parametros
   
   Example
   -------
   >>> obtener_poblacion_paises(datos_poblacion, param_paises = {"Spain"})
    { 'Spain':
        {
          1997: 39967802
          1998: 40202000
          ...
        }
     }
   """
   if datos_poblacion == {} or param_paises == {}:
       raise ValueError("Error. El diccionario y/o los parametros de consulta estan vacios")
     
   param_paises = interseccion(param_paises, set(datos_poblacion.keys()))
   return {pais: datos_poblacion[pais] for pais in param_paises}

def obtener_poblacion_annos(datos_poblacion, param_annos):
    """
    Funcion auxiliar que recupera los valores de poblacion,
    para todos los paises, en el/los anno/s dado/s
    AVISO: Si NO encuentra resultados, devuelve un diccionario
    vacio ({})

    Parameters
    ----------
    datos_poblacion : dict
        Diccionario con los datos completos
        de poblacion
    param_annos : set(int)
        Conjunto con los annos a consultar
        en el diccionario

    Returns
    -------
    dict
        Diccionario con los datos de poblacion
        en el/los anno/s pasado/s como argumento/s
    
    Precondition
    ------------
    El diccionario pasado como parametro NO debe estar vacio, asi como
    tambien sus parametros
    
    Example
    -------
    >>> obtener_poblacion_annos(datos_poblacion, param_annos = {1998,2001})
    { 'Spain':
        {
          1998: 40202000,
          2001: 41319000
        },
     'France':
       {
         1998: 40202000,
         2001: 41319000
       }
     }
     """   
    if datos_poblacion == {} or param_annos == {}:
      raise ValueError("Error. El diccionario y/o los parametros de consulta estan vacios")
     
    diccionario = dict()
    for pais, annos_poblacion in datos_poblacion.items():
        if interseccion(param_annos, set(annos_poblacion)) != []:
            diccionario[pais] = parejas_annos_poblacion(param_annos, annos_poblacion)
     
    return diccionario
        
def obtener_poblacion_paises_annos(datos_poblacion, param_paises, param_annos):
    """
    Funcion que devuelve los valores
    de poblacion en un/os pais/es y/o
    anno/s dado/s como argumentos
    AVISO: Si NO encuentra resultados, devuelve un diccionario
    vacio ({})

    Parameters
    ----------
    datos_poblacion : dict
        Diccionario con los datos completos
        de poblacion
    param_paises : set(str)
        Conjunto con los paises a consultar
    param_annos : set(int)
        Conjunto con los annos a consultar

    Returns
    -------
    dict
        Diccionario con los datos de poblacion
        en el/los anno/s pasado/s y/o pais/es
        pasado/s como argumento/s
    
    Example
    -------
    >>> obtener_poblacion_annos(datos_poblacion, param_pais = {"Spain"} param_annos = {1998})
    { 'Spain':
        {
          1998: 40202000
        }
     }

    """   
    if datos_poblacion == {} or param_annos == {}:
      raise ValueError("Error. El diccionario y/o los parametros de consulta estan vacios")
    
    param_paises = interseccion(param_paises, set(datos_poblacion.keys()))
    
    diccionario = dict()
    for pais in param_paises:
        if interseccion(param_annos, set(datos_poblacion[pais])) != []:
            diccionario[pais] = parejas_annos_poblacion(param_annos, datos_poblacion[pais])
     
    return diccionario

def parejas_annos_poblacion(param_annos, annos_poblacion):
    """
    Funcion auxiliar que recupera las parejas annos:poblacion
    por cada pais

    Parameters
    ----------
    param_annos : set(int)
        Conjunto con los annos a filtrar, pasados
        como parametro en obtener_poblacion()
    annos_poblacion : dict
        Diccionario con los annos y poblacion disponibles,
        de los cuales se filtraran aquellos
        incluidos en param_annos

    Returns
    -------
    dict
        Diccionario con las parejas anno: poblacion filtradas
        segun param_annos

    """
    return {anno: annos_poblacion[anno] for anno in interseccion(param_annos, set(annos_poblacion))}

def interseccion(subconjunto1, subconjunto2):
    """
    Funcion que devuelve la interseccion ordenada de 
    ambos elementos

    Parameters
    ----------
    subconjunto1 : set
    subconjunto1 : set

    Returns
    -------
   list
        Interseccion (annos comunes) entre ambos parametros

    Example
    -------
    >> subconjunto({1998, 1999, -10000}, {1998, 1999})
    {1998, 1999}
    """
    return sorted(subconjunto1 & subconjunto2)

def evolucion_poblacion(datos_poblacion, fecha_ini, fecha_fin):
    """
    Funcion que calcula la evolucion de la poblacion de
    un pais entre dos annos dados

    Parameters
    ----------
    datos_poblacion : dict
        Diccionario con los datos de la poblacion
        en cada anno
    fecha_ini, fecha_fin, intervalo: int
        Fecha de inicio, fin
        
    Returns
    -------
    dict
        Diccionario con la evolucion historica
    
    Precondition
    ------------
    El diccionario debe contener DIRECTAMENTE las parejas annos, poblacion
    del pais en particular
    
    El diccionario NO debe estar vacio
    
    fecha_ini < fecha_fin
        La fecha de inicio debe ser estrictamente menor a la fecha fin
    
    Example
    -------
    >> calcular_evolucion_poblacion(datos_poblacion.get('Europe'), 1998, 1999)
    {
     1998 y 1999: 79444992
     }
    """    
    if datos_poblacion == {}:
        raise ValueError("Error. El diccionario esta vacio")
    elif fecha_ini > fecha_fin:
        raise ValueError("Error. La fecha de inicio debe ser menor a la fecha de fin")
    
    annos_comunes = {fecha_ini, fecha_fin} - set(datos_poblacion)
    
    if annos_comunes != set():
        conjunto_paises = str(sorted(datos_poblacion.keys()))
        raise ValueError("Error. Lista de posibles paises/annos de uso: \n" + conjunto_paises)
    
    diccionario = dict()
    diccionario[str(fecha_ini)+" y "+str(fecha_fin)] = datos_poblacion[fecha_fin] - datos_poblacion[fecha_ini]
    
    return diccionario