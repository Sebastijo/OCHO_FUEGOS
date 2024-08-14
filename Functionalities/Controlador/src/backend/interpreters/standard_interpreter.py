"""
El objetivo de este modulo es definir la función interpreter_standard.


Empresa: Ocho Fuegos
Autor: Sebastián P. Pincheira
Fecha: 10/01/2024
Lenguaje: Python 3.11.7
Librerías:
- pandas: 2.2.0
- numpy: 1.24.2
- sympy: 1.12
# - tabula: 2.9.0
"""

# Importación de librerías
import pandas as pd
import numpy as np
import sympy as sp
from typing import Union

# import tabula
import os
import re

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


def interpreter_standard(liquidacion: Union[str, pd.DataFrame]) -> tuple[list, list]:
    """
    Esta función interpreta los datos de un archivo de liquidación y devuelve una tupla con las siguientes coordenadas:
    los formatos válidos de liquidaciones son: 8F (standard).

    0) Lista de listas con la informacion de la liquidación.
    1) Lista de enteros con las páginas de la liquidación (en este caso, [1])

    Args:
        liquidacion (str or pd.DataFrame): Ruta del archivo de liquidación o DataFrame con la liquidación.

    Returns:
        list: Lista de listas con los datos de la liquidación.

    Raises:
        AssertionError: Si el archivo no es str o pd.DataFrame.
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

    def simplifier(x):
        """
        Takes a string x of the form f"{expression}KG" and return f"{simplified}KG"
        Example: simplifier("2*2.5KG") -> "5KG"

        Args:
            x (str): The string to be simplified

        Returns:
            str: The simplified string
        """
        if isinstance(x, str):
            x = x.upper()
            if x == "nan":
                return np.nan
            else:
                # Remove all letters and spaces
                expression = re.sub(r"[a-zA-Z\s]", "", x)
                # Simplify the expression
                simplified = sp.simplify(expression)
                # Remove unnecessary decimal places
                simplified = (
                    str(simplified).rstrip("0").rstrip(".")
                    if "." in str(simplified)
                    else str(simplified)
                )
                # Return the simplified expression
                return str(simplified) + "KG"
        elif isinstance(x, (int, float)):
            if not np.isnan(x):
                simplified = str(x).rstrip("0").rstrip(".") if "." in str(x) else str(x)
                return str(simplified) + "KG"
            else:
                return np.nan
        else:
            return np.nan if np.isnan(x) else str(x)

    # Leemos el archivo
    if isinstance(liquidacion, str):
        liquidacion_df = pd.read_excel(liquidacion, dtype=str)
    else:
        liquidacion_df = liquidacion

    # Encontramos la tabla main
    assert (
        "观察" in liquidacion_df.iloc[:, 0].values
        or "货品" in liquidacion_df.iloc[:, 0].values
    ), f"La tabla principal no fue encontrada en el archivo {liquidacion}: no existe la columna '{'观察'}' ni '{'货品'}' en la columna 1 del archivo .xlsx."
    if "观察" in liquidacion_df.iloc[:, 0].values:
        main_location = liquidacion_df[liquidacion_df.iloc[:, 0] == "观察"].index[0]
        liquidacion_df = liquidacion_df.iloc[main_location:]
    if "货品" in liquidacion_df.iloc[:, 0].values:
        main_location = liquidacion_df[liquidacion_df.iloc[:, 0] == "货品"].index[0]
        liquidacion_df = liquidacion_df.iloc[main_location:]

    # Establecemos los nombres de la columna
    liquidacion_df.columns = liquidacion_df.iloc[0]
    liquidacion_df = liquidacion_df.iloc[2:].reset_index(drop=True)

    # Nos quedamos con las columnas que nos interesan
    assert all(
        [
            col in liquidacion_df.columns
            for col in set(main_dict_liq_standard.keys() - {"CSG"} - {"观察"})
        ]  # Algunos no tienen "观察" (Observacion)
    ), f"Las columnas de la tabla principal del archivo {liquidacion} no son las correctas. Deben ser {list(main_dict_liq_standard.keys())}."
    assert (
        "CSG" in liquidacion_df.columns or "销售数量" in liquidacion_df.columns
    ), f"La columna 'CSG' o '销售数量' no fue encontrada en el archivo {liquidacion}: no existe la columna '{'CSG'}' ni '{'销售数量'}' en el archivo .xlsx."

    # Si existe la columna sales boxes, le cambiamos el nombre por CSG para que se mantenga la columna (nos importa para cost), luego la eliminaremos
    se_remplazo_sales_boxes_por_CSG = False
    if "销售数量" in liquidacion_df.columns:
        liquidacion_df = liquidacion_df.rename(columns={"销售数量": "CSG"})
        se_remplazo_sales_boxes_por_CSG = True

    wanted_columns = list(
        set(main_dict_liq_standard.keys()) & set(liquidacion_df.columns)
    )
    wanted_columns = list(
        sorted(
            wanted_columns, key=lambda x: list(main_dict_liq_standard.keys()).index(x)
        )
    )

    if list(liquidacion_df.columns)[0] in wanted_columns:
        liquidacion_df = liquidacion_df[wanted_columns]
    else:
        liquidacion_df = liquidacion_df[
            [list(liquidacion_df.columns)[0], *wanted_columns]
        ]

    # Renombramos las columnas y establecemos las columnas que queremos
    liquidacion_df = liquidacion_df.rename(columns=main_dict_liq_standard)
    wanted_columns = [main_dict_liq_standard[column] for column in wanted_columns]

    assert (
        "total" in liquidacion_df.iloc[:, 0].values
    ), f"La fila de totales no fue encontrada en el archivo {liquidacion}: no existe la fila '{'total'}' en la columna 1 del archivo .xlsx."

    summary_location = liquidacion_df[liquidacion_df.iloc[:, 0] == "total"].index[0]

    liquidacion_df = liquidacion_df[wanted_columns]
    # Definimos la tabla de costo (removemos las "liquidations")

    cost = (
        (
            liquidacion_df.iloc[summary_location + 1 :]
            .dropna(how="all")
            .dropna(axis=1, how="all")
            .reset_index(drop=True)
        )
        .iloc[:-1]
        .copy()
    )

    if "LOCALIDAD" in cost.columns:
        cost = cost.drop(columns="LOCALIDAD")

    if se_remplazo_sales_boxes_por_CSG:
        liquidacion_df = liquidacion_df.drop(columns=["果园 CSG"])

    # Definimos la tabla main
    main = (
        liquidacion_df.iloc[: summary_location + 1]
        .dropna(how="all")
        .dropna(axis=1, how="all")
        .reset_index(drop=True)
    ).copy()

    # si una caja tiene masa "2*2.5KG", por ejemplo, se remplaza por "5KG"
    main["规格 Specification"] = main["规格 Specification"].apply(simplifier)

    # Definimos la tabla de notas
    note = pd.DataFrame(columns=["Note:"])

    # Hacemos cambios para que coincida con el formato general
    main["每箱收益 FOB FOB Return"] = 0
    main["总收益 FOB Total Return"] = 0

    null_checker = lambda x: (x in {0, "0"} or (isinstance(x, float) and np.isnan(x)))
    main["价格 (人民币) Price RMB"] = main["价格 (人民币) Price RMB"].replace(
        "-", np.nan
    )
    main.loc[
        ~main["数量 Quantity"].apply(null_checker)
        & main["价格 (人民币) Price RMB"].apply(null_checker),
        "日期 Date",
    ] = "No vendido"
    main.loc[main.index[-1], "日期 Date"] = np.nan

    # Simplifacamos los pesos de las cajas (ej: 2*2.5KG -> 5KG)

    # Borramos la columna en chino
    for column in cost.columns:
        pattern = r"[^A-Za-z0-9.]|(?<=\')np\.nan(?=\')"
        contains_non_american = cost[column].astype(str).str.contains(pattern, na=False)
        if contains_non_american.all():
            cost = cost.drop(columns=column)
            break

    cost.columns = ["其他费用 Additional Fees", "人民币 RMB", "美金 USD"]

    # Posicionamos donde corresponde (al final)
    assert any(
        "commission" in str(value).lower()
        for value in cost["其他费用 Additional Fees"].values
    ), f"La fila de comisión no fue encontrada en el archivo {liquidacion}: no existe una fila que contenga '{'Commission'}' en el archivo .xlsx."

    commission_location = cost[
        cost["其他费用 Additional Fees"].str.contains("commission", case=False)
    ].index[0]

    cost_rows = list(range(cost.shape[0]))

    assert (
        commission_location in cost_rows
    ), f"La posición de comission ({commission_location}) no se encuentra en los indices de las columnas de costo ({cost_rows})"
    commission_location = cost_rows.pop(commission_location)
    cost_rows.append(commission_location)
    cost = cost.reindex(cost_rows).reset_index(drop=True)

    # Definimos la comision
    commission = (
        float(cost.at[cost.shape[0] - 1, "美金 USD"])
        / float(main.at[main.index[-1], "总数 (美金) Total USD"])
    ) * 100
    commission = round(commission, 1)
    try:
        commission = int(commission)
    except:
        commission = commission
    # Renombramos la fila de comisión
    cost.at[cost.shape[0] - 1, "其他费用 Additional Fees"] = (
        f"销售佣金 Commission ({commission}%)"
    )

    # Definimos la fila de total fees
    for column in ["人民币 RMB", "美金 USD"]:
        cost[column] = pd.to_numeric(
            cost[column].str.replace(",", "").str.replace("[()]", ""), errors="coerce"
        ).fillna(0)

    total_fees_RMB = cost["人民币 RMB"].iloc[: cost.shape[0] - 1].sum()
    total_fees_USD = cost["美金 USD"].iloc[: cost.shape[0] - 1].sum()

    for column in ["人民币 RMB", "美金 USD"]:
        cost[column] = cost[column].astype(str)

    total_fees = pd.DataFrame(
        {
            "其他费用 Additional Fees": ["小计 Total Fees"],
            "人民币 RMB": [total_fees_RMB],
            "美金 USD": [total_fees_USD],
        }
    )
    cost = pd.concat([cost.head(cost.shape[0] - 1), total_fees, cost.tail(1)])

    # Definimos la fila de total charges
    total_charges = pd.DataFrame(
        {
            "其他费用 Additional Fees": ["总费用 Total Charges"],
            "人民币 RMB": [
                float(cost["人民币 RMB"].iloc[-1]) + float(cost["人民币 RMB"].iloc[-2])
            ],
            "美金 USD": [
                float(cost["美金 USD"].iloc[-1]) + float(cost["美金 USD"].iloc[-2])
            ],
        }
    )
    cost = pd.concat([cost, total_charges]).reset_index(drop=True)

    assert any(
        "vat" in str(value).lower() for value in cost["其他费用 Additional Fees"].values
    ), "No se pudo encontrar la fila de arancel adicional: no se encontró la fila que contenga 'VAT' en la columna '其他费用 Additional Fees'."

    main["LOCALIDAD"] = main["LOCALIDAD"].replace("nan", np.nan)

    liquidacion_list = [[main, cost, note]]

    return liquidacion_list, [1]
