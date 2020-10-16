# -*- coding: utf-8 -*-
"""
@author: alberto
"""
#apartado i)
from mrjob.job import MRJob
import json
import os
import sys


class MRComputoFallecimientos(MRJob):
    """
    clase MRComputoFallecimientos. Representa los metodos map, reduce
    para el calculo de fallecimientos por cada causa
    """
    def mapper(self, _, line):
        """
        Metodo mapper encargado de generar las parejas clave, valor,
        es decir, la causa de fallecimiento junto el total de fallecidos
        por cada pais
        """
        linea = line.split()
        causa, fallecidos = linea[0], linea[1]
        fallecidos_f = float(fallecidos)
        
        yield causa, (1, round(fallecidos_f))
    
    def reducer(self, key, values):
        """
        Metodo reducer encargado de sumar los valores, agrupados por clave,
        mediante la funcion suma_parejas
        """
        yield key, suma_parejas(values)

def suma_parejas(pares):
    """
    Funcion auxiliar encargada de sumar parejas de valores con la misma
    clave (causa de fallecimiento)
    """
    a, b = 0, 0
    for x, y in pares:
        a, b = a + x, b + y
    return a, b

def crear_diccionario(archivo):
    """
    Funcion encargada de aplicar el metodo map-reduce sobre el contenido
    del archivo

    Parameters
    ----------
    archivo : str
        Nombre del archivo a consultar

    Returns
    -------
    diccionario : dict
        Diccionario con las parejas causa_fallecimiento, total_fallecimientos
        resultantes de aplicar el metodo map-reduce
    """
    trabajo = MRComputoFallecimientos(args=[archivo])
    diccionario = dict()
    with trabajo.make_runner() as runner:
        runner.run()
        for causa, fallecimientos in trabajo.parse_output(runner.cat_output()):
            diccionario[causa] = fallecimientos[1]
            
    return diccionario    

# Ejecucion por terminal
if __name__ == '__main__':
    """
    El fichero de entrada:
        debe estar situado en el directorio actual
        debe estar en formato txt
        NO debe estar vacio
    """
    mensaje_error = "Error. Uso correcto: python total_fallecimientos.py -i parejas.txt"
    if len(sys.argv) != 3:
        print(mensaje_error)
        sys.exit(1)
    
    parametros = sys.argv[1]
    if parametros != "-i":
        print(mensaje_error)
        sys.exit(1)
    
    fichero = sys.argv[2]
    
    if not os.path.exists(fichero):
        raise FileNotFoundError("Error. El fichero no se encuentra en el directorio actual")
        
    elif not fichero.endswith('.txt'):
        raise Exception("Error. El fichero debe estar en formato txt")
    
    elif os.stat(fichero).st_size == 0:
        raise StopIteration("Error. El fichero esta vacio")
    
    print(json.dumps(crear_diccionario(fichero), indent=4))