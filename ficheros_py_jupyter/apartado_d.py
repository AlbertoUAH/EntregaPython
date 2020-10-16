"""
@author: alberto
"""
# apartado d)
import matplotlib.pyplot as plt
from matplotlib import rc
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
    Subplot1, Subplot2
        Graficas comparativas entre los valores del pais seleccionado y la poblacion mundial

    Precondition
    ------------
    Ambos DataFrames:
        deben tener el mismo numero de filas
        deben contener valores numericos
    """     
    try:
        if len(df_evolucion_poblacion_mundial) != len(df_evolucion_poblacion_pais):
            raise ValueError("Error. Las tablas no presentan el mismo numero de filas")
        
        pobl_min_pais, pobl_max_pais = int(df_evolucion_poblacion_pais.min()), int(df_evolucion_poblacion_pais.max())
        pobl_min_glob, pobl_max_glob = int(df_evolucion_poblacion_mundial.min()), int(df_evolucion_poblacion_mundial.max())
        formula = lambda poblacion: ((poblacion - pobl_min_pais) / (pobl_max_pais - pobl_min_pais)) * (pobl_max_glob - pobl_min_glob) + pobl_min_glob
        
        return imprimir_grafica(df_evolucion_poblacion_mundial, df_evolucion_poblacion_pais.apply(formula))
    except TypeError:
        print("Error. El DataFrame contiene valores NO numericos")

def imprimir_grafica(df_evolucion_poblacion_mundial, df_evolucion_poblacion_pais):
    """
    Funcion que imprime un grafico comparativo entre ambos DataFrames

    Parameters
    ----------
    df_evolucion_poblacion_mundial : pandas.DataFrame
        DataFrame con los datos de la poblacion mundial
    df_evolucion_poblacion_pais : pandas.DataFrame
        DataFrame con los datos escalados de la poblacion de un pais

    Returns
    -------
    ax1, ax2 : Subplots
        Graficas comparativas con los datos de ambos DataFrames
    """
    pais = list(df_evolucion_poblacion_pais.columns)
    
    rc("font", weight = "bold")
    figura, (ax1, ax2) = plt.subplots(2, figsize = (12,12))
    
    plt.ticklabel_format(useOffset=False)
    ax1.plot(df_evolucion_poblacion_mundial, c="blue", linewidth=2.0)
    ax2.plot(df_evolucion_poblacion_pais, c="orange", linewidth=2.0)
    
    ax1.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax2.xaxis.set_major_locator(MaxNLocator(integer=True))
    
    ax2.set_xlabel("Años", fontsize=15)
    ax1.set_ylabel("Total poblacion (x $10^9$)", fontsize=15)
    ax2.set_ylabel("Total poblacion (re-escalado)", fontsize=15)
    
    ax1.legend(["Evolucion poblacion mundial"], loc="best")
    ax2.legend(["Evolucion poblacion -pais: " + pais[0] + "-"], loc="best")
    
    plt.suptitle("Comparativa entre los valores de la población mundial y los valores re-escalados de la poblacion en " + pais[0], fontsize = 15)
    plt.style.use('ggplot')
    
    return ax1, ax2