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
        r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\pickles\pseudo_control.pkl"
    )
    liquidacion_pickle = (
        r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\pickles\liquidacion.pkl"
    )
    errores_pickle = (
        r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\pickles\errores.pkl"
    )

    revisar_pickle = (
        r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\pickles\revisar.pkl"
    )

# Variables globales
key_liq = var.key_liq
key_liq_incompleto = var.key_liq_incompleto


def control(
    embarques_path: str,
    facturas_path: str,
    tarifa_path: str,
    liquidaciones_path: str,
    update_loading_bar: callable = None,
) -> tuple[pd.DataFrame, dict, dict]:
    """
    Recibe los paths de los archivos de embarques (.xlsx), facturas (.xlsx), tarifa (.xlsx) y liquidaciones (folder)
    devuelve una tupla conteniendo:

    0) Un dataframe con el control final
    1) Un diccionario con los errores de liquidación
    2) Un diccionario con los elementos que necesitan ser revisados

    Args:
        embarques_path (str): path del archivo de embarques
        facturas_path (str): path del archivo de facturas
        tarifa_path (str): path del archivo de tarifa
        liquidaciones_path (str): path del folder de liquidaciones

    Returns:
        tuple[pd.DataFrame, dict, dict]: Un dataframe con el control final y un diccionario con los errores de liquidación

    Raises:
        AssertionError: Si alguno de los paths no es un string o no existe.
        AssertionError: Si alguno de los paths de embarques_path, facturas_path, tarifa_path no es un archivo.
        AssertionError: Si el path de liquidaciones_path no es un directorio.
    """

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
            liquidacion, _, _ = liquidaciones(liquidaciones_path)
            with open(liquidacion_pickle, "wb") as file:
                pkl.dump(liquidacion, file)

        if os.path.exists(errores_pickle):
            with open(errores_pickle, "rb") as file:
                errores = pkl.load(file)
        else:
            _, errores, _ = liquidaciones(liquidaciones_path)
            with open(errores_pickle, "wb") as file:
                pkl.dump(errores, file)

        if os.path.exists(revisar_pickle):
            with open(revisar_pickle, "rb") as file:
                revisar = pkl.load(file)
        else:
            _, _, revisar = liquidaciones(liquidaciones_path)
            with open(revisar_pickle, "wb") as file:
                pkl.dump(revisar, file)

    else:
        for input in [embarques_path, facturas_path, tarifa_path, liquidaciones_path]:
            assert (
                type(input) == str
            ), f"La ruta del archivo '{input}' no es una cadena de texto."
            assert os.path.exists(input), f"La ruta del archivo '{input}' no existe."
            if input == liquidaciones_path:
                assert os.path.isdir(input) or input.lower().endswith(
                    (".pdf")
                ), f"'{input}' no es una carpeta ni un archivo de PDF."
            else:
                assert os.path.isfile(
                    input
                ), f"'{input}' no es una archivo; puede que sea una carpeta."
                assert input.lower().endswith(
                    (".xlsx", ".xls")
                ), f"El archivo '{input}' no es un archivo de Excel."

        # Contamos la cantidad de operaciones que se realizarán (una por archivo)
        if update_loading_bar:
            if os.path.isdir(liquidaciones_path):
                liquidations = len(os.listdir(liquidaciones_path))
            else:
                liquidations = 1
            total_operations = 1 + 3 + 2 + liquidations
        else:
            total_operations = 0
        if update_loading_bar:  # 1ra operacion
            update_loading_bar(1 / total_operations * 100)
        pseudo_control = pseudoControl(
            embarques_path,
            facturas_path,
            tarifa_path,
            update_loading_bar,
            total_operations,
        )
        if update_loading_bar:  # 5ta operacion
            update_loading_bar(1 / total_operations * 100)
        liquidacion, errores, revisar = liquidaciones(
            liquidaciones_path, update_loading_bar, total_operations
        )
        if update_loading_bar: # 6ta operacion
            update_loading_bar(1 / total_operations * 100)

    if __name__ == "__main__":
        # Resumen de los inputs:
        duplicate_elements = (
            pseudo_control[pseudo_control.duplicated(key_liq)][key_liq]
            .drop_duplicates()
            .reset_index(drop=True)
        )
        print("Embarques en pseudocontrol =", pseudo_control.shape[0])
        print("Key_liq duplicado en pseudo_control =", duplicate_elements.shape[0])
        suma_sin = 0
        suma_con = 0
        for embarque in liquidacion:
            if embarque.CSG:
                suma_con += embarque.main.shape[0]
            else:
                suma_sin += embarque.main.shape[0]
        print("Embarques sin CSG en liquidaciones =", suma_sin)
        print("Embarques con CSG en liquidaciones =", suma_con)
        print("Embarques totales en liquidaciones =", suma_sin + suma_con)

    # Separamos las liquidaciones con y sin CSG
    liq_con_CSG = []
    liq_sin_CSG = []
    for embarques in liquidacion:
        # Eliminamos las columnas "CAJAS" y "KG NET/CAJA" de las liquidaciones
        embarques.main = embarques.main.drop(columns=["KG NET/CAJA"])
        if embarques.CSG:
            liq_con_CSG.append(embarques.main)
        else:
            liq_sin_CSG.append(embarques.main)

    # Si no hay liquidaciones con CSG o sin CSG, entonces el control final es el pseudo control con las columnas de liquidación vacías.
    if len(liq_sin_CSG) + len(liq_con_CSG) == 0:
        control_df = pseudo_control
        for column in [
            "FECHA VENTA",
            "FOLIO",
            "CSG",
            "VARIEDAD",
            "CALIBRES",
            "CAJAS LIQUIDADAS",
            "RMB/CJ",
            "TOTAL RMB",
            "TOTAL USD",
            "RETORNO FOB/CJ",
            "RETORNO FOB",
            "COSTO",
            "COSTO/CJ",
            "COSTO/KG",
            "COMISION",
            "COMISION/CJ",
            "COMISION/KG",
            "COSTO Y COMISION",
            "LIQ FINAL",
        ]:
            control_df[column] = None
    else:
        # Concatenamos las liquidaciones con y sin CSG
        if len(liq_con_CSG) > 0: # Si hay liquidaciones con CSG
            liquidacion_con_CSG = pd.concat(liq_con_CSG)
            control_df = pseudo_control.merge(
                liquidacion_con_CSG,
                how="left",
                on=key_liq,
            )
            if len(liq_sin_CSG) > 0: 
                liquidacion_sin_CSG = pd.concat(liq_sin_CSG)
                control_df = control_df.merge(
                    liquidacion_sin_CSG,
                    how="left",
                    on=key_liq_incompleto,
                    suffixes=("_con", "_sin"),
                )
        else: # Si no hay liquidaciones con CSG
            liquidacion_sin_CSG = pd.concat(liq_sin_CSG)
            control_df = pseudo_control.merge(
                liquidacion_sin_CSG,
                how="left",
                on=key_liq_incompleto,
            )

        # Juntamos las columnas duplicadas
        sin_list = [
            columnSin for columnSin in control_df.columns if columnSin.endswith("_sin")
        ]
        con_list = [
            columnCon for columnCon in control_df.columns if columnCon.endswith("_con")
        ]
        for columnSin, columnCon in zip(sin_list, con_list):
            assert (
                columnSin[:-4] == columnCon[:-4]
            ), f"Se intentó emparejar las columnas {columnSin} y {columnCon} pero estas no coinciden."
            column = columnSin[:-4]
            pair = control_df[[columnSin, columnCon]]
            assert (
                pair.isnull().any(axis=1).all()
            ), f"Hay un elemento en las liquidaciones que aparece dos veces: una vez con columna CSG y otra con columna CSG."
            control_df.drop(columns=[columnSin, columnCon], inplace=True)
            control_df[column] = pair.apply(
                lambda row: (
                    row[columnSin] if pd.isnull(row[columnCon]) else row[columnCon]
                ),
                axis=1,
            )

    return (
        control_df,
        errores,
        revisar,
    )


if __name__ == "__main__":
    control_df, errores, revisar = control(
        embarques_path_, facturas_path_, tarifa_path_, liquidaciones_path_
    )

    control_df.dropna(subset=["TOTAL USD"], inplace=True)
    control_df.reset_index(inplace=True, drop=True)

    print("Control:")
    print(control_df)
    print()
    print("Errores:")
    print(errores)
    print("Por revisar:")
    print(revisar)
