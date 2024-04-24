"""
El objetivo de este módulo es interpretar los archivos de liquidación de HFF_SEA y ajustarlos al formato HFF para luego ser usados en liquidacion_HFF.

Empresa: Ocho Fuegos
Autor: Sebastián P. Pincheira
Fecha: 10/01/2024
Lenguaje: Python 3.11.7
Librerías:
- pandas: 2.2.0
- numpy: 1.24.2
- sympy: 1.12
- tabula: 2.9.0
"""

# Importación de librerías
import pandas as pd
import numpy as np

# import tabula
import os

# importamos modulos porpios
if __name__ == "__main__":
    from src.config import variables as var
else:
    from ...config import variables as var

# Definimos variables globales
main_dict_liq_standard = var.main_dict_liq_standard
main_dict_liq_JF = var.main_dict_liq_JF
main_list_liq_HFF = var.main_list_liq_HFF
main_list_liq_HFF_SEA = var.main_list_liq_HFF_SEA


def interpreter_HFF_SEA(liquidacion: str) -> pd.DataFrame:
    """
    Esta función tiene como objetivo ajustar el formato de la liquidacion de HFF SEA al formato HFF para luego ser usados en liquidacion_HFF.

    Args:
        liquidacion (str): Ruta del archivo de liquidación.

    Return:
        pd.DataFrame: DataFrame con el formato de liquidacion HFF.

    Raises:
        AssertionError: Si el archivo de liquidación no existe, no es un archivo o no es un archivo .xlsx o .xls.
    """
    assert os.path.exists(liquidacion), f"El archivo '{liquidacion}' no existe."
    assert os.path.isfile(liquidacion), f"El archivo '{liquidacion}' no es un archivo."
    assert liquidacion.endswith(
        (".xlsx", ".xls")
    ), f"El archivo '{liquidacion}' no es un archivo .xlsx o .xls."

    RMB_to_USD = 7.30

    # Leemos el archivo
    liquidacion_df = pd.read_excel(liquidacion, dtype=str)

    # Encontramos la tabla main
    assert (
        "货品" in liquidacion_df.iloc[:, 0].values
    ), f"La tabla principal no fue encontrada en el archivo {liquidacion}: no existe la columna '{'货品'}' en la columna 1 del archivo .xlsx."
    main_location = liquidacion_df[liquidacion_df.iloc[:, 0] == "货品"].index[0]
    localidad = liquidacion_df.iloc[main_location - 3, 1][-2:]
    liquidacion_df = liquidacion_df.iloc[main_location:].reset_index(drop=True)

    # Establecemos los nombres de las columnas como la primera fila
    # Arreglamos el nombre de la columna "每箱收益 FOB FOB Return": la eliminamos
    liquidacion_df.columns = liquidacion_df.iloc[0]
    assert (
        liquidacion_df.columns[-2] == "金额"
    ), f"No se encontró la columna FOB en la liquidación {liquidacion}."
    duplicate_column = liquidacion_df["金额"].copy()
    duplicate_column = duplicate_column.iloc[:, 0]
    liquidacion_df.drop(columns="金额", inplace=True)
    liquidacion_df = pd.concat([liquidacion_df, duplicate_column], axis=1)
    liquidacion_df["到货数量"] = np.nan
    liquidacion_df["金额"] = pd.to_numeric(liquidacion_df["金额"], errors="coerce")
    liquidacion_df["美金"] = liquidacion_df["金额"].apply(
        lambda x: (
            str(
                "{:.2f}".format(round(float(x) / RMB_to_USD, 2)).rstrip("0").rstrip(".")
            )
            if not str(x) in ["金额", "Total（RMB）", str(np.nan)]
            else (
                "美金"
                if x == "金额"
                else "Total（USD）" if x == "Total（RMB）" else np.nan
            )
        )
    )
    liquidacion_df["金额"] = liquidacion_df["金额"].astype(str)
    liquidacion_df["美金"] = liquidacion_df["美金"].astype(str)
    assert set(list(main_list_liq_HFF_SEA.keys())).issubset(
        set(liquidacion_df.columns)
    ), f"Las columnas de la tabla principal del archivo {liquidacion} no son las correctas. Deben ser {list(main_list_liq_HFF_SEA)}."
    liquidacion_df = liquidacion_df[list(main_list_liq_HFF_SEA.keys())]
    liquidacion_df.rename(columns=main_list_liq_HFF_SEA, inplace=True)

    # Buscamos la columna cost
    assert (
        len(
            [
                value
                for value in liquidacion_df["销售数量"].values
                if "commission" in str(value).lower()
            ]
        )
        > 0
    ), f"La fila de commission no fue encontrada en el archivo {liquidacion}: no existe la fila '{'commission'}' en la columna {'销售数量'} del archivo .xlsx."
    for index, value in liquidacion_df["销售数量"].items():
        if "commission" in str(value).lower():
            # If "commission" is found, print the index and break the loop
            commission_location = index
            summary_location = commission_location - 1
            break

    cost = liquidacion_df.iloc[summary_location + 1 :].copy()
    main = liquidacion_df.iloc[: summary_location + 1].copy()

    main["到货数量"] = main["销售数量"]
    last_index = main["尺寸"].index[-1]
    main.at[last_index, "观察"] = "total"
    columns_to_sum = {"到货数量", "销售数量"}
    for column in columns_to_sum:
        main.at[last_index, column] = pd.to_numeric(
            main[column][2:-1], errors="coerce"
        ).sum()
        main[column] = main[column].astype(str)
        main[column] = main[column].apply(
            lambda x: str(x).rstrip("0").rstrip(".") if "." in str(x) else str(x)
        )
    main.at[last_index, "尺寸"] = np.nan
    main["LOCALIDAD"] = "LOCALIDAD"
    main.loc[1:, "LOCALIDAD"] = localidad

    cost["尺寸"] = np.nan
    cost["单价"] = np.nan
    cost = cost.iloc[:-1]

    assert any(
        "add-value duty" in str(value).lower() for value in cost["销售数量"].values
    ), "No se pudo encontrar la fila de arancel adicional: no se encontró la fila que contenga 'Add-Value Duty' en la columna '销售数量'."

    liquidacion_df = pd.concat([main, cost])
    liquidacion_df.iloc[0] = liquidacion_df.columns
    
    return liquidacion_df
