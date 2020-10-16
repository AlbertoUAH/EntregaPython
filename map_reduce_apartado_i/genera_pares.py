# -*- coding: utf-8 -*-
"""
@author: alberto
"""
#apartado i)
import sys
import apartado_e
import apartado_h

COLUMNA_ANNO = 'Year'
COLUMNA_PAIS = 'Entity'

def generar_pares(df_fallecimientos, param_anno, columnas, archivo):
    """
    Funcion encargada de generar parejas (causa_fallecimiento, numero_fallecimientos)
    por cada fila de la tabla de datos, dado un anno como parametro. 
    El resultado final es volcado en el archivo indicado por el usuario

    Parameters
    ----------
    df_fallecimientos : pandas.DataFrame
        DataFrame con los valores de mortalidad en los distintos paises y annos
    param_anno : int
        Anno a consultar
    columnas : set
        Conjunto de columnas con las causas de fallecimiento a calcular
    archivo: str
        Nombre del archivo donde volcar el resultado
    
    Preconditions
    -------------
    El archivo debe tener formato .txt
    El conjunto de columnas deben exitir en el DataFrame
    """
    
    if not archivo.endswith('.txt'):
        raise Exception("Error. El fichero debe estar en formato txt")
    
    df_fallecimientos = apartado_e.filtrar_tabla(df_fallecimientos, COLUMNA_ANNO, {param_anno})
    
    if not columnas.issubset(df_fallecimientos.columns):
        raise KeyError("Error. La/s causa/s de mortalidad seleccionada/s no existe/n como columna/s")
    
    df_fallecimientos = df_fallecimientos[columnas]
    
    lista_parejas = [generar_parejas(columnas,fila) for fila in df_fallecimientos.values.tolist()]
    
    with open(archivo, "w") as f:
        for combinaciones in lista_parejas:
            for parejas in combinaciones:
                f.write(" ".join(str(elemento).replace(' ','-') for elemento in parejas) + "\n")
        


def generar_parejas(columnas, fila):
    """
    Funcion auxiliar que devuelve un listado con las parejas 
    (causa_fallecimiento, numero_fallecimientos) de una fila
    de la tabla de datos

    Parameters
    ----------
    columnas : set
        Conjunto de columnas con las causas de fallecimiento
    fila : list
        Lista con el numero de fallecimientos de un pais

    Returns
    -------
    list
        Lista formada por las parejas (causa_fallecimiento, numero_fallecimientos)
        de una fila de la tabla en particular
    """
    return [[columna, valor] for columna, valor in zip(columnas, fila)]

def preprocesar_tabla_datos(fichero):
    """
    Funcion encargada de cargar los datos y realizar un primer preprocesamiento,
    eliminando signos de comparacion ('>1000' o '>1')

    Parameters
    ----------
    fichero : str
        Ruta del fichero .csv

    Returns
    -------
    df_fallecimientos : pandas.DataFrame
        Tabla pre-procesada, con los valores de fallecimientos por pais y anno
    """
    
    df_fallecimientos = apartado_e.causas_fallecimiento(fichero)

    for columna in df_fallecimientos.columns:
            df_fallecimientos[columna] = apartado_e.eliminar_caracter(df_fallecimientos[columna],'[>]+')
        
    return df_fallecimientos

# Ejecucion por terminal
if __name__ == '__main__':
    """
    El comando de ejecucion debe tener el siguiente formato:
        python genera_pares.py -i fichero_entrada.csv -y anno {-r regiones.txt}
        
        -> -i fichero_entrada.csv => fichero de datos de entrada
        -> -y anno => anno a consultar el total de fallecimientos
        -> -r regiones.txt => fichero con las regiones a eliminar (OPCIONAL)
    """
    mensaje_error = "Error. Uso correcto: python genera_pares.py -i fichero_entrada.csv -y anno {-r regiones.txt}"
    
    if len(sys.argv) != 5 and len(sys.argv) != 7:
        print(mensaje_error)
        sys.exit(1)
    
    parametros = [sys.argv[1], sys.argv[3]]
    if parametros != ["-i", "-y"]:
        print(mensaje_error)
        sys.exit(1)
    
    fichero = sys.argv[2]
    anno = sys.argv[4]
    df_fallecimientos = preprocesar_tabla_datos(fichero)
    
    if len(sys.argv) == 7:
        if(sys.argv[5] != "-r"):
            print(mensaje_error)
            sys.exit(1)
        columnas = sys.argv[6]
        df_fallecimientos = apartado_h.eliminar_filas(df_fallecimientos, COLUMNA_PAIS, columnas)
        
    df_fallecimientos = df_fallecimientos._get_numeric_data()
    generar_pares(df_fallecimientos, int(anno), set(df_fallecimientos.columns) - {COLUMNA_ANNO}, "parejas.txt")