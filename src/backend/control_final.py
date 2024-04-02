"""
El objetivo de esrte modulo es juntar el control sin liquidacines producido en el modulo embarque.py con la liquidación producida en el modulo liquidacion_reader.py
Empresa: Ocho Fuegos
Autor: Sebastián P. Pincheira
Fecha: 28/01/2024
Lenguaje: Python 3.11.7
Librerías:
- pandas: 2.2.0
- numpy: 1.26.3
"""

import pandas as pd
import numpy as np
import os
import pickle as pkl

# Importamos modulos propios
if __name__ == "__main__":
    import shutil

    destination_datos_del_programa = (
        r"C:\\Users\\spinc\\Desktop\\OCHO_FUEGOS\\src\\backend\\Datos del programa"
    )
    source_datos_del_programa = r"C:\Users\spinc\Desktop\OCHO_FUEGOS\Datos del programa"
    if not os.path.exists(destination_datos_del_programa):
        shutil.copytree(source_datos_del_programa, destination_datos_del_programa)

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
        r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\Base embarques.xlsx"
    )
    facturas_path_ = (
        r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\Facturas proformas.xlsx"
    )
    tarifa_path_ = r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\Tarifas.xlsx"

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
) -> tuple[pd.DataFrame, dict, dict, pd.DataFrame]:
    """
    Recibe los paths de los archivos de embarques (.xlsx), facturas (.xlsx), tarifa (.xlsx) y liquidaciones (folder)
    devuelve una tupla conteniendo:

    0) Un dataframe con el control final
    1) Un diccionario con los errores de liquidación
    2) Un diccionario con los elementos que necesitan ser revisados
    3) Liquidaciones no pareadas

    Args:
        embarques_path (str): path del archivo de embarques
        facturas_path (str): path del archivo de facturas
        tarifa_path (str): path del archivo de tarifa
        liquidaciones_path (str): path del folder de liquidaciones

    Returns:
        tuple[pd.DataFrame, dict, dict, pd.DataFrame, pd.DataFrame]: Un dataframe con el control final y un diccionario con los errores de liquidación

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
        # Revisamos que el input sean archivos y que estos existan
        for input in [embarques_path, facturas_path, tarifa_path, liquidaciones_path]:
            assert (
                type(input) == str
            ), f"La ruta del archivo '{input}' no es una cadena de texto."
            assert os.path.exists(input), f"La ruta del archivo '{input}' no existe."
            if input == liquidaciones_path:
                assert (
                    os.path.isdir(input)
                    or input.lower().endswith(".pdf")
                    or input.lower().endswith(".xlsx")
                    or input.lower().endswith(".xls")
                ), f"'{input}' no es una carpeta ni un archivo de PDF ni un archivo Excel."
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
            total_operations = 1 + 4 + 2 + liquidations
        else:
            total_operations = 0
        if update_loading_bar:  # 1ra operacion
            update_loading_bar(1 / total_operations * 100)

        # Creamos el pseudocontrol
        pseudo_control = pseudoControl(
            embarques_path,
            facturas_path,
            tarifa_path,
            update_loading_bar,
            total_operations,
        )

        if update_loading_bar:  # 5ta operacion
            update_loading_bar(1 / total_operations * 100)

        # Creamos la liquidaciones
        liquidacion, errores, revisar = liquidaciones(
            liquidaciones_path, update_loading_bar, total_operations
        )

        if update_loading_bar:  # 6ta operacion
            update_loading_bar(1 / total_operations * 100)

    # Separamos las liquidaciones con y sin CSG
    liq_con_CSG = []
    liq_sin_CSG = []
    liquidaciones_no_pareadas = pd.DataFrame()
    for embarques in liquidacion:
        if embarques.CSG:
            liq_con_CSG.append(embarques.main)
        else:
            liq_sin_CSG.append(embarques.main)

    # Si no hay liquidaciones, entonces el control final es el pseudo control con las columnas de liquidación vacías.
    if len(liq_sin_CSG) + len(liq_con_CSG) == 0:
        control_df = pseudo_control
        for column in [
            "UBICACIÓN",
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
        no_vendidos_con_CSG = pd.DataFrame()
        no_vendidos_sin_CSG = pd.DataFrame()
        liquidaciones_sin_CSG_no_pareadas = pd.DataFrame()
        liquidaciones_con_CSG_no_pareadas = pd.DataFrame()

        for liquidacion in liq_con_CSG + liq_sin_CSG:
            liquidacion["KG NET/CAJA"] = liquidacion["KG NET/CAJA"].astype(str)

        # Concatenamos las liquidaciones con y sin CSG
        if len(liq_con_CSG) > 0:  # Si hay liquidaciones con CSG
            liquidacion_con_CSG = pd.concat(liq_con_CSG)
            control_df = pseudo_control.merge(
                liquidacion_con_CSG,
                how="left",
                on=key_liq,
            )

            # Obtenemos las liquidaciones con CSG no pareadas
            liquidaciones_con_CSG_no_pareadas = liquidacion_con_CSG.merge(
                pseudo_control, how="left", on=key_liq, indicator=True
            )

            liquidaciones_con_CSG_no_pareadas = liquidaciones_con_CSG_no_pareadas[
                list(liquidacion_con_CSG.columns) + ["_merge"]
            ]
            liquidaciones_con_CSG_no_pareadas = liquidaciones_con_CSG_no_pareadas[
                liquidaciones_con_CSG_no_pareadas["_merge"] == "left_only"
            ]

            if len(liq_sin_CSG) > 0:
                liquidacion_sin_CSG = pd.concat(liq_sin_CSG)
                control_df = control_df.merge(
                    liquidacion_sin_CSG,
                    how="left",
                    on=key_liq_incompleto,
                    suffixes=("_con", "_sin"),
                )

                # Obtenemos las liquidaciones sin CSG no pareadas
                liquidaciones_sin_CSG_no_pareadas = liquidacion_sin_CSG.merge(
                    pseudo_control, how="left", on=key_liq_incompleto, indicator=True
                )
                # print("No pareadas",list(liquidaciones_sin_CSG_no_pareadas.columns))
                liquidaciones_sin_CSG_no_pareadas = liquidaciones_sin_CSG_no_pareadas[
                    list(liquidacion_sin_CSG.columns) + ["_merge"]
                ]
                liquidaciones_sin_CSG_no_pareadas = liquidaciones_sin_CSG_no_pareadas[
                    liquidaciones_sin_CSG_no_pareadas["_merge"] == "left_only"
                ]

        else:  # Si no hay liquidaciones con CSG
            liquidacion_sin_CSG = pd.concat(liq_sin_CSG)
            control_df = pseudo_control.merge(
                liquidacion_sin_CSG,
                how="left",
                on=key_liq_incompleto,
            )

            # Obtenemos las liquidaciones sin CSG no pareadas
            liquidaciones_sin_CSG_no_pareadas = liquidacion_sin_CSG.merge(
                pseudo_control, how="left", on=key_liq_incompleto, indicator=True
            )
            liquidaciones_sin_CSG_no_pareadas = liquidaciones_sin_CSG_no_pareadas[
                list(liquidacion_sin_CSG.columns) + ["_merge"]
            ]
            liquidaciones_sin_CSG_no_pareadas = liquidaciones_sin_CSG_no_pareadas[
                liquidaciones_sin_CSG_no_pareadas["_merge"] == "left_only"
            ]

        # Obtenemos las liquidaciones no pareadas
        liquidaciones_sin_CSG_no_pareadas["CSG"] = np.nan
        liquidaciones_no_pareadas = pd.DataFrame()
        if (
            len(liquidaciones_sin_CSG_no_pareadas)
            + len(liquidaciones_con_CSG_no_pareadas)
            > 0
        ):
            if len(liquidaciones_con_CSG_no_pareadas) > 0:
                if len(liquidaciones_sin_CSG_no_pareadas) > 0:
                    liquidaciones_no_pareadas = pd.concat(
                        [
                            liquidaciones_con_CSG_no_pareadas,
                            liquidaciones_sin_CSG_no_pareadas,
                        ]
                    )
                else:
                    liquidaciones_no_pareadas = liquidaciones_con_CSG_no_pareadas
            else:
                liquidaciones_no_pareadas = liquidaciones_sin_CSG_no_pareadas

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

    df_output = [control_df, liquidaciones_no_pareadas]
    for idx, df in enumerate(df_output):
        df_output[idx].replace(
            {str(np.nan).upper(): np.nan, "NAN": np.nan}, inplace=True
        )

    # Cambiamos el formato de las fechas
    def convert_to_date(value):
        try:
            return pd.to_datetime(value).strftime("%Y-%m-%d")
        except ValueError:
            return value

    date_columns = [
        "FECHA FACTURA",
        "FECHA DESPACHO PLANTA",
        "FECHA EMBALAJE",
        "ETD",
        "ETA",
        "ETD REAL",
        "ETA REAL",
        "FECHA VENTA",
    ]
    for column in date_columns:
        df_output[0][column] = df_output[0][column].apply(convert_to_date)

    control_order = [
        col for col in control_df.columns if col not in ["COSTO SECO/KG"]
    ] + ["COSTO SECO/KG"]
    control_df = control_df[control_order]

    liquidaciones_no_pareadas = liquidaciones_no_pareadas.drop(columns=["_merge"])
    liquidaciones_no_pareadas = liquidaciones_no_pareadas[liquidaciones_no_pareadas["CAJAS LIQUIDADAS"] != 0]

    for df in [control_df, liquidaciones_no_pareadas]:
        df.reset_index(drop=True, inplace=True)

    return (
        control_df,
        errores,
        revisar,
        liquidaciones_no_pareadas,
    )


if __name__ == "__main__":
    control_df, errores, revisar, liquidaciones_no_pareadas = control(
        embarques_path_, facturas_path_, tarifa_path_, liquidaciones_path_
    )
    shutil.rmtree(destination_datos_del_programa)

    print("Control:")
    print(control_df)
    print()
    print("Errores:")
    print(errores)
    print("Por revisar:")
    print(revisar)
    print("Liquidaciones no pareadas:")
    print(liquidaciones_no_pareadas)
