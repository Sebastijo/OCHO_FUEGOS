"""
El objetivo de este modulo es crear una función que revise y notifique errores en las liquidaciones.
Empresa: Ocho Fuegos
Autor: Sebastián P. Pincheira
Fecha: 28/01/2024
Lenguaje: Python 3.11.7
Librerías:
- pandas: 2.2.0
"""

# Importamos paquetes
import pandas as pd

# Importamos modulos propios
if __name__ == "__main__":
    from src.backend.embarque_liquidacion_class import embarqueL
else:
    from .embarque_liquidacion_class import embarqueL

# Creamos una lista de liquidaciones de ejemplo
if __name__ == "__main__":
    from src.backend.liquidacion_reader import liquidaciones as liquidaciones_maker
    import os
    import pickle as pk

    liquidaciones_path = r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\Liquidaciones\All 8F Sales Summary (1).pdf"
    liquidaciones_pickle = r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\pickles\All_8F_Sales_Summary_(1)_as_embaruqeL_list.pkl"

    if os.path.exists(liquidaciones_pickle):
        with open(liquidaciones_pickle, "rb") as file:
            liquidaciones = pk.load(file)
    else:
        (liquidaciones, _) = liquidaciones_maker(liquidaciones_path)
        with open(liquidaciones_pickle, "wb") as file:
            pk.dump(liquidaciones, file)

    liquidacion_ejemplo = liquidaciones[-3]


def revisar_liquidacion(liquidacion: embarqueL) -> tuple[bool, list]:
    """
    Recibe una liquidación y revisa si hay errores en la liquidación misma.
    Retorna una tupla con un booleano y un string:

    0) Un booleano equivalente a "hay inconsistencias en la liquidación"
    1) Una lista con las inconsistencias encontrados; posterioremnte serán despliegados en la GUI

    Args:
        liquidacion (EmbarqueL): Liquidación a revisar

    Returns:
        tuple[bool, list]: Tupla con un booleano y una lista de inconsistencias

    Raises:
        AssertionError: Si liquidacion no es una instancia de embarqueL
    """
    assert isinstance(liquidacion, embarqueL)

    main = liquidacion.main
    main_summary = liquidacion.main_summary
    cost = liquidacion.cost
    commission = liquidacion.commission
    commission_value = liquidacion.commission_value

    inconsistencias = []
    epsilon = 5e-1  # Tolerancia para comparar floats
    # REVISAMOS SI HAY INCONSISTENCIAS EN LA LIQUIDACIÓN:

    # Revisamos que el Total Fees esté bien calculado
    fees_index = cost.index.get_loc("Total Fees")  # Índice de Total Fees
    total_fees = cost.iloc[:fees_index].sum()  # Total Fees a mano
    if not abs(total_fees["USD"] - cost.loc["Total Fees", "USD"]) < epsilon:
        inconsistencias.append("'Total Fees' no coincide con la suma de los fees.")

    # Revisamos que la suma de Total USD esté bien calculada
    total_usd = main["TOTAL USD"].sum()
    if not abs(total_usd - main_summary["TOTAL USD"].iloc[0]) < epsilon:
        inconsistencias.append(
            "La suma de 'Total USD' no coincide con la suma de los valores de 'TOTAL USD'."
        )

    # Revisamos que la comision esté bien calculada
    comision_valor = total_usd * commission
    if not abs(comision_valor - commission_value) < epsilon:
        inconsistencias.append(
            f"El valor de la comisión, en USD, no coincide con el {100*commission}% de la suma de la columna 'Total USD'."
        )

    # Revisamos que los Total Charges estén bien calculados
    charges_index = cost.index.get_loc("Total Charges")  # Índice de Total Charges
    total_charges = comision_valor + total_fees
    if not abs(total_charges["USD"] - cost.loc["Total Charges", "USD"]) < epsilon:
        inconsistencias.append(
            "'Total Charges' no coincide con la suma de los fees y la comisión."
        )

    # Revisamos que los Retornos FOB estén bien calculados
    retorno_fob = main["RETORNO FOB"].sum()
    if not abs(retorno_fob - main_summary["RETORNO FOB"].iloc[0]) < epsilon:
        inconsistencias.append(
            "La suma de 'RETORNO FOB' no coincide con la suma de los valores de 'RETORNO FOB'."
        )
    # Definimos hay_incosnistencias
    if len(inconsistencias) == 0:
        hay_inconsistencias = False
    else:
        hay_inconsistencias = True

    return hay_inconsistencias, inconsistencias


# Testeamos la función
if __name__ == "__main__":
    it_works = True
    liquidaciones_inconsistencias = []
    for liquidacion in liquidaciones:
        idx = liquidacion.location
        #try:
        (hay_inconsistencias, _) = revisar_liquidacion(liquidacion)
        if hay_inconsistencias:
            liquidaciones_inconsistencias.append(idx)
        #except Exception as e:
            #print(f"La función tuvo problemas interpretando la liquidacion {idx}: {e}")
            #it_works = False
    print("Información general:")
    print(
        "La función revisar_liquidacion interpreta correctamente las liquidaciones:",
        it_works,
    )
    print("Embarques con inconsistencias:", liquidaciones_inconsistencias)
    print("Cantidad de embarques con inconsistencias:", len(liquidaciones_inconsistencias))
    print()
    hay_inconsistencias, inconsistencias = revisar_liquidacion(liquidacion_ejemplo)
    print("Información del embarque de ejemplo:")
    print("Hay inconsistencias:", hay_inconsistencias)
    print("Lista de inconsistencias:", inconsistencias)
