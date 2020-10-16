"""
@author: alberto
"""
# apartado j) y k.2)
from matplotlib import cm
from matplotlib import rc
import matplotlib.pyplot as plt
import pandas as pd
import apartado_e

def mostrar_numero_fallecidos(df_fallecimientos, param_pais, param_anno, escala):
    """
    Funcion que muestra el numero de fallecidos en un pais y anno (segun una escala)

    Parameters
    ----------
    df_fallecimientos : pandas.DataFrame
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
        Grafico de barras final, con el numero de fallecidos por cada causa
        
    Preconditions
    -------------
    La escala solo puede ser lineal (linear) o logaritmica (log)
    """
    df_causas_fallecimiento = pd.merge(apartado_e.filtrar_tabla(df_fallecimientos, ENTITY, {param_pais}),\
                                       apartado_e.filtrar_tabla(df_fallecimientos, YEAR, {param_anno}), how = "inner")
    
    df_causas_fallecimiento = df_causas_fallecimiento._get_numeric_data().drop(YEAR, axis = 1)
    if escala not in ["linear", "log"]:
        raise ValueError("Error. La escala solo puede ser lineal (linear) o logaritimica (log)")
    
    traspuesta = df_causas_fallecimiento.T.sort_values(0)
    traspuesta = traspuesta[~(traspuesta == 0).any(axis=1)]
    
    lista_colores = cm.get_cmap("viridis", len(traspuesta))
    grafico_barras = imprimir_grafico_barras(traspuesta.index, traspuesta[0], lista_colores.colors[::-1])
    
    for indice, valor in enumerate(traspuesta[0]):
            plt.text(valor, indice, formatear_numero(valor), verticalalignment="center", fontsize = 10)
    
    plt.title("Comparativa valores mortalidad. Pais: " + param_pais + ". Año: " + str(param_anno), fontweight="bold")
    plt.xlabel("Total fallecimientos. Escala - " + escala, fontweight="bold")
    plt.xscale(escala)
    plt.grid(axis='x', linestyle = '--')
    plt.yticks(fontsize = 13)
    
    return plt.show()
	
def formatear_numero(numero):
    """
    Funcion que permite dar formato a un numero para su representacion grafica.
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
        Numero con el formato especifico (en funcion de si es del orden de millones o no)
    
    Example
    -------
    >>> formatear_numero(2145234)
    2.15 Mill.
    """
    if numero >= 10**6:
        return str(round(numero / 10**6, 2)) + " Mill."
    else:
        return format(round(numero), ",")