"""
El objetivo de este módulo es interpretar los archivos de liquidación de HFF y ajustarlos al formato standard para luego ser usados en liquidacion_standard.

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
from typing import Union

# import tabula
import os

# importamos modulos porpios
if __name__ == "__main__":
    from src.config import variables as var
    from src.backend.interpreters.standard_interpreter import interpreter_standard
else:
    from ...config import variables as var
    from .standard_interpreter import interpreter_standard


# Definimos variables globales
main_dict_liq_standard = var.main_dict_liq_standard
main_dict_liq_JF = var.main_dict_liq_JF
main_list_liq_HFF = var.main_list_liq_HFF
main_list_liq_HFF_SEA = var.main_list_liq_HFF_SEA


def interpreter_HFF(liquidacion: Union[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Esta función tiene como objetivo ajustar el formato de la liquidacion de HFF al formato standard para luego ser usados en liquidacion_standard.

    Args:
        liquidacion (str or pd.DataFrame): Ruta del archivo de liquidación o DataFrame con la liquidación.

    Returns:
        pd.DataFrame: DataFrame con el formato de liquidacion standard.

    Raises:
        AssertionError: Si liquidacion no es str o pd.DataFrame.
        AssertionError: Si el archivo de liquidación no existe, no es un archivo o no es un archivo .pdf o .xlsx.
        AssertionError: Si la tabla principal no fue encontrada en el archivo .xlsx.
        AssertionError: Si las columnas de la tabla principal del archivo .xlsx no son las correctas.
        AssertionError: Si la fila de totales no fue encontrada en el archivo .xlsx.
        AssertionError: Si la posición de comission no se encuentra en los indices de las columnas de costo.
    """
    assert isinstance(
        liquidacion, (str, pd.DataFrame)
    ), f"El argumento liquidacion debe ser un string o un DataFrame, no {type(liquidacion)}."
    if isinstance(liquidacion, str):
        assert os.path.exists(liquidacion), f"El archivo '{liquidacion}' no existe."
        assert os.path.isfile(
            liquidacion
        ), f"El archivo '{liquidacion}' no es un archivo."
        assert liquidacion.endswith(
            (".xlsx", ".xls")
        ), f"El archivo '{liquidacion}' no es un archivo .xlsx o .xls."

        # Leemos el archivo
        liquidacion_df = pd.read_excel(liquidacion, dtype=str)
    else:
        liquidacion_df = liquidacion
    # Encontramos la tabla main
    assert (
        "观察" in liquidacion_df.iloc[:, 0].values
    ), f"La tabla principal no fue encontrada en el archivo {liquidacion}: no existe la columna '{'观察'}' en la columna 1 del archivo .xlsx."
    main_location = liquidacion_df[liquidacion_df.iloc[:, 0] == "观察"].index[0]
    liquidacion_df = liquidacion_df.iloc[main_location:].reset_index(drop=True)

    # Establecemos los nombres de las columnas como la primera fila
    liquidacion_df.columns = liquidacion_df.iloc[0]
    assert (
        set(main_list_liq_HFF) - set(liquidacion_df.columns) == set()
    ), f"Las columnas de la tabla principal del archivo {liquidacion} no son las correctas. Deben ser {list(main_list_liq_HFF)}."
    liquidacion_df = liquidacion_df[main_list_liq_HFF]

    # Buscamos la columna cost
    assert (
        "total" in liquidacion_df.iloc[:, 0].values
    ), f"La fila de totales no fue encontrada en el archivo {liquidacion}: no existe la fila '{'total'}' en la columna 1 del archivo .xlsx."
    summary_location = liquidacion_df[liquidacion_df.iloc[:, 0] == "total"].index[0]
    cost = liquidacion_df.iloc[summary_location + 1 :].copy()
    main = liquidacion_df.iloc[: summary_location + 1].copy()

    # Remplazamos el nombre de VAT
    assert any(
        "add-value duty" in str(value).lower() for value in cost["销售数量"].values
    ), "No se pudo encontrar la fila de arancel adicional: no se encontró la fila que contenga 'Add-Value Duty' en la columna '销售数量'."
    VAT_location = cost[
        cost["销售数量"].str.contains("add-value duty", case=False, na=False)
    ].index[0]
    cost.at[VAT_location, "销售数量"] = "VAT"

    # Remplazamos la columna boxes por CSG (np.nan)
    assert "CSG" not in main.columns, "La columna 'CSG' ya existe en el archivo."
    main.rename(columns={"到货数量": "CSG"}, inplace=True)
    main["CSG"] = "CSG"
    main.loc[2:, "CSG"] = np.nan

    # Cambiamos el nombre de la columna sales boxes por la de boxes
    main = main.rename(columns={"销售数量": "到货数量"})
    main.iloc[0] = main.columns

    # Cambiamos los nombres de las columnas de cost para que estén en la posición deseada así tambíen el orden de main
    cost = cost.rename(columns={"销售数量": "CSG"})
    main = main[cost.columns]

    liquidacion_df = pd.concat([main, cost])

    return interpreter_standard(liquidacion_df)
