"""
@author: alberto
"""
# apartado b)
def interseccion(subconjunto1, subconjunto2):
    """
    Funcion que devuelve la interseccion ordenada de ambos elementos

    Parameters
    ----------
    subconjunto1 : set
    subconjunto2 : set

    Returns
    -------
    list
        Interseccion (paises/annos comunes) entre ambos parametros

    Example
    -------
    >> subconjunto({1998, 1999, -10000}, {1998, 1999})
    {1998, 1999}
    """
    return sorted(subconjunto1 & subconjunto2)
	
def parejas_annos_poblacion(param_annos, annos_poblacion):
    """
    Funcion auxiliar que recupera las parejas annos:poblacion, cuyos annos
    esten incluidos en param_annos

    Parameters
    ----------
    param_annos : set
        Conjunto con los annos a filtrar
    annos_poblacion : dict
        Diccionario con los annos y poblacion disponibles

    Returns
    -------
    dict
        Diccionario con las parejas anno: poblacion filtradas segun param_annos
        
    Example
    -------
    >>> parejas_annos_poblacion({1998}, {1998: 40543123, 1999: 41546343})
    {
        1998: 40543123
    }

    """
    return {anno: annos_poblacion[anno] for anno in interseccion(param_annos, set(annos_poblacion))}
	
def obtener_poblacion_paises_annos(datos_poblacion, param_paises, param_annos):
    """
    Funcion que devuelve los valores de poblacion en un/os pais/es y
    anno/s dado/s como argumentos. AVISO: Si NO encuentra resultados, 
    devuelve un diccionario vacio ({})

    Parameters
    ----------
    datos_poblacion : dict
        Diccionario con los datos completos de poblacion
    param_paises : set
        Conjunto con los paises a consultar
    param_annos : set
        Conjunto con los annos a consultar

    Returns
    -------
    dict
        Diccionario con los datos de poblacion en el/los anno/s pasado/s y pais/es
        pasado/s como argumentos
        
    Precondition
    ------------
    El diccionario y los parametros de consulta, NO deben estar vacios '{}'
    Debe filtrarse, al menos, un subconjunto de param_paises y param_annos
    
    Example
    -------
    >>> obtener_poblacion_annos(datos_poblacion, param_pais = {"Spain"} param_annos = {1998})
    { 'Spain':
        {
          1998: 40202000
        }
     }
    """
    if datos_poblacion == {} or param_paises == {} or param_annos == {}:
      raise ValueError("Error. El diccionario y/o los parametros de consulta estan vacios")

    paises = interseccion(param_paises, set(datos_poblacion.keys()))

    diccionario = dict()
    for pais in paises:
        if interseccion(param_annos, set(datos_poblacion[pais])) != []:
            diccionario[pais] = parejas_annos_poblacion(param_annos, datos_poblacion[pais])
    if diccionario == {}:
       raise ValueError("Error. No se han encontrado valores para " + str(param_paises) + "," + str(param_annos)) 
    return diccionario

def evolucion_poblacion(datos_poblacion, fecha_ini, fecha_fin):
    """
    Funcion que calcula la evolucion de la poblacion de un pais entre dos annos dados

    Parameters
    ----------
    datos_poblacion : dict
        Diccionario con los datos de la poblacion en cada anno
    fecha_ini, fecha_fin: int
        Fecha de inicio, fin
        
    Returns
    -------
    dict
        Diccionario con la evolucion historica
    
    Precondition
    ------------
    El diccionario debe contener DIRECTAMENTE las parejas annos, poblacion del pais en particular
    El diccionario NO debe estar vacio
    fecha_ini < fecha_fin
        La fecha de inicio debe ser estrictamente menor a la fecha fin
    Si no existen los annos a consutar, devuelve un listado con los annos disponibles
    
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

    elif any(str(clave).isalpha() for clave in list(datos_poblacion.keys())):
        raise ValueError("Error. Debe indicar directamente el conjunto de annos,poblacion. Ej: datos_poblacion.get('Europe')")

    annos_comunes = {fecha_ini, fecha_fin} - set(datos_poblacion)
    if annos_comunes != set():
        conjunto_disponible = str(sorted(datos_poblacion.keys()))
        raise ValueError("Error. Los annos seleccionados no estan disponibles. Listado de annos disponibles: \n" + conjunto_disponible)

    return {str(fecha_ini)+" y "+str(fecha_fin): datos_poblacion[fecha_fin] - datos_poblacion[fecha_ini]}