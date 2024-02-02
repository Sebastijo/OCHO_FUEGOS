"""
El objetivo de esrte modulo es juntar el control sin liquidacines producido en el modulo embarque.py con la liquidación producida en el modulo liquidacion_reader.py
Empresa: Ocho Fuegos
Autor: Sebastián P. Pincheira
Fecha: 28/01/2024
Lenguaje: Python 3.11.7
Librerías:
- pandas: 2.2.0
"""

import pandas as pd
import os
import pickle as pkl

# Importamos modulos propios
if __name__ == "__main__":
    from src.config import variables as var
    from src.backend.embarques import pseudoControl
    from src.backend.liquidacion_reader import liquidaciones
else:
    from ..config import variables as var
    from ..backend.embarques import pseudoControl
    from ..backend.liquidacion_reader import liquidaciones

if __name__ == "__main__":
    # Paths to your input files
    embarques_path_ = (
        r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\base_embarques.xlsx"
    )
    facturas_path_ = (
        r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\facturas_proformas.xlsx"
    )
    tarifa_path_ = r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\tarifa_aerea.xlsx"

    liquidaciones_path_ = r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\Liquidaciones"

    # Picle location
    pseudo_control_pickle = (
        r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\pseudo_control.pkl"
    )
    liquidacion_pickle = (
        r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\liquidacion.pkl"
    )
    errores_pickle = r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\errores.pkl"

# Variables globales
key_liq = var.key_liq
key_liq_incompleto = var.key_liq_incompleto


def control(
    embarques_path: str, facturas_path: str, tarifa_path: str, liquidaciones_path: str
) -> tuple[pd.DataFrame, dict]:
    if (
        __name__ == "__main__"
        and embarques_path == embarques_path_
        and facturas_path == facturas_path_
        and tarifa_path == tarifa_path_
        and liquidaciones_path == liquidaciones_path_
    ):
        if os.path.exists(pseudo_control_pickle):
            pseudo_control = pd.read_pickle(pseudo_control_pickle)
        else:
            pseudo_control = pseudoControl(embarques_path, facturas_path, tarifa_path)
            pseudo_control.to_pickle(pseudo_control_pickle)

        if os.path.exists(liquidacion_pickle):
            with open(liquidacion_pickle, "rb") as file:
                liquidacion = pkl.load(file)
        else:
            liquidacion, _ = liquidaciones(liquidaciones_path)
            with open(liquidacion_pickle, "wb") as file:
                pkl.dump(liquidacion, file)

        if os.path.exists(errores_pickle):
            with open(errores_pickle, "rb") as file:
                errores = pkl.load(file)
        else:
            _, errores = liquidaciones(liquidaciones_path)
            with open(errores_pickle, "wb") as file:
                pkl.dump(errores, file)
    else:
        pseudo_control = pseudoControl(embarques_path, facturas_path, tarifa_path)
        liquidacion, errores = liquidaciones(liquidaciones_path)

    # Creamos las columnas claves para el merge mediante tuples
    pseudo_control["key_con_CSG"] = pseudo_control.apply(
        lambda row: tuple(row[key_liq]), axis=1
    )
    pseudo_control["key_sin_CSG"] = pseudo_control.apply(
        lambda row: tuple(row[key_liq_incompleto]), axis=1
    )
    for embarque in liquidacion:
        if embarque.CSG:
            embarque.main["key_con_CSG"] = embarque.main.apply(
                lambda row: tuple(row[key_liq]), axis=1
            )
        else:
            embarque.main["key_sin_CSG"] = embarque.main.apply(
                lambda row: tuple(row[key_liq_incompleto]), axis=1
            )

    print("Embarques totales = ", pseudo_control.shape[0])
    suma_sin = 0
    suma_con = 0
    for embarque in liquidacion:
        if embarque.CSG:
            suma_con += embarque.main.shape[0]
        else:
            suma_sin += embarque.main.shape[0]
    print("suma sin =", suma_sin)
    print("suma con =", suma_con)
    print("suma total =", suma_sin + suma_con)

    print(liquidacion[-1].main.shape[0])

    # Mergeamos los dataframes
    liq_con_CSG = []
    liq_sin_CSG = []
    for embarques in liquidacion:
        if embarques.CSG:
            liq_con_CSG.append(embarques.main)
        else:
            liq_sin_CSG.append(embarques.main)

    liquidacion_con_CSG = pd.concat(liq_con_CSG)
    liquidacion_sin_CSG = pd.concat(liq_sin_CSG)

    control_df = pseudo_control.merge(
        liquidacion_con_CSG,
        how="left",
        on="key_con_CSG",
        suffixes=("_pseudo", "_liq"),
    )

    control_df = control_df.merge(
        liquidacion_sin_CSG,
        how="left",
        on="key_sin_CSG",
        suffixes=("_pseudo", "_liq"),
    )

    return control_df, errores


if __name__ == "__main__":
    control_df, errores = control(
        embarques_path_, facturas_path_, tarifa_path_, liquidaciones_path_
    )

    # control_df = control_df.dropna(subset=["TOTAL USD"])

    print("Control:")
    print(control_df)
    print()
    print("Errores:")
    print(errores)
