"""
El objetivo de este módulo es intepretar los distintos tipos de liquidaciones que se pueden realizar en el sistema.
Los tipos de liquidaciones disponibles son:

    - 12Islands (.pdf)
    - JumboFruit (.xlsx)
    - 8F (.xlsx)
    - Happy Farm Fruit (.xlsx)

El resultado de el módulo es producir una lista de listas, cada lista representando un embarque y los elementos de la lista representadno los diversos datos presentes en un embarque.
Cada formato tendrá su función que lo traduce. Los formatos se relacionan de la siguiente manera.

-
-Happy Farm Fruit (HFF) es traducido al formato standard 8F.
-Jumbo Fruit (BQ) es traducido al formmato standard 8F.
-El formato standard 8F es traducido al formato 12Islands.

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
import sympy as sp
from typing import Union
import tabula
import os
import re

# importamos modulos porpios
if __name__ == "__main__":
    from src.config import variables as var
else:
    from ..config import variables as var


# Definimos variables globales
main_dict_liq_standard = var.main_dict_liq_standard
main_dict_liq_JF = var.main_dict_liq_JF
main_list_liq_HFF = var.main_list_liq_HFF
main_list_liq_HFF_SEA = var.main_list_liq_HFF_SEA

if __name__ == "__main__":
    example1 = r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\Liquidaciones\HT_Sales Summary 020-30475115-Ocho Fuegos-1-1 .xlsx"
    example2 = r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\Liquidaciones\BQ_Sales Report-8F-AIR-045-91458345-X.xlsx"


def interpreter_12Islands(liquidacion: str) -> tuple[list, list]:
    """
    Two inputs possible: PDF or Excel file
    For PDF:
    Takes in a liquidación file in the forma of a PDF in the format of the 12Islands liquidation format (can have multimple embarques)
    For Excel:
    Takes in a liquidación file in the format of the 12Islands liquidation format.

    Returns tuple with two coordinates:

    0) A list of lists, the n-th list contains the tables, as DataFrames, corresponding to the n-th embarque.
    1) A list of integers, the n-th integer is the page number of the first page of the n-th embarque.

    Args:
        liquidaciones_folder (str): Path to the liquidaciones folder

    Returns:
        tuple: tuple with two coordinates (list, list)

    Raises:
        AssertionError: If the path does not exist
        AssertionError: If the path is not a PDF file
        AssertionError: If the number of tables in a page is not 1 or >= 3
        AssertionError: If the embarque index is not correct: In each cycle, it should be the last index of embarques or the last index of embarques plus 1
    """
    assert os.path.exists(liquidacion), f"La ruta del archivo {liquidacion} no existe."
    assert os.path.isfile(liquidacion) and liquidacion.lower().endswith(
        (".pdf", ".xlsx", ".xls")
    ), f"El archivo {liquidacion} no es un archivo .pdf, .xlsx, o xls."

    embarques = []  # Lista de todos los embarques

    paginas_list = (
        []
    )  # Lista cuya n-ésima entrada contiene la primera página del n-ésimo embarque
    if liquidacion.endswith(".pdf"):
        embarqueNum = 0  # Índice del embarque en la lista de embarques
        i = 0  # Índice de página (pagina - 1)
        pages_left = True
        while pages_left:  # Recorremos hasta que no queden hojas
            embarque_change = False  # "El embarque cambió respecto al ciclo anterior"
            while not embarque_change:  # Mientras nos mantengamos en el mismo embarque
                """
                Las páginas del PDF contienen distintos embarques, cada embarque puede estar contenido en varias págnas las cuales están una tras la otra.
                Este while se encarga de identificar los diferentes embarques y poner todas las tablas de un mismo embarque en una misma msima lista metida en la lista embarques.
                """
                page = i + 1  # Definimos la página actual a partir del índice

                try:
                    # Transformamos la página en una lista de tablas DataFrame

                    tables_in_page = tabula.read_pdf(
                        liquidacion,
                        pages=page,
                        multiple_tables=True,
                        pandas_options={"dtype": str},
                    )

                except Exception as e:  # Si no hay hojas restantes, terminamos
                    assert (
                        str(e)
                        == "java.lang.IndexOutOfBoundsException: Page number does not exist."
                    ), f"Error de lecutra del PDF de liquidacion {liquidacion}: {e}"
                    pages_left = False
                    break

                assert (
                    embarqueNum == len(embarques) or embarqueNum == len(embarques) - 1
                ), "El índice de embarque no es correcto"
                if embarqueNum == len(
                    embarques
                ):  # Si el embarque no existe, lo creamos y guardamos su núemro de página
                    embarques.append(tables_in_page)
                    paginas_list.append(page)

                elif (
                    embarqueNum == len(embarques) - 1
                ):  # Si el embarque si existe, lo agregamos
                    embarques[embarqueNum] = embarques[embarqueNum] + tables_in_page
                cardinality = len(tables_in_page)  # Cantidad de tables en la hoja
                assert (
                    cardinality >= 3 or cardinality == 1
                ), f"La cantidad de tablas en la página {page} del archivo {liquidacion} no es correcta; deberían srer una o más que tres."
                if (
                    cardinality >= 3
                ):  # Si es la última página de embarque, cambiamos de embarque
                    embarqueNum += 1
                    embarque_change = True
                i += 1  # Pasamos a la siguiente pagina

    else:  # Si el archivo es un excel
        embarque = pd.read_excel(liquidacion, dtype=str)
        embarque = embarque.dropna(axis=1, how="all")

        main_location = embarque[embarque.iloc[:, 0] == "日期"].index[0]
        embarque = embarque.iloc[main_location:].reset_index(drop=True)

        concatenated_string = embarque.iloc[0] + " " + embarque.iloc[1]
        embarque.columns = concatenated_string
        embarque = embarque.iloc[2:]
        embarque.reset_index(drop=True, inplace=True)

        embarque.columns = [
            column.replace(" " + " ", " ")
            .replace("(", " (")
            .replace("FOB FOB", " FOB FOB")
            for column in list(embarque.columns)
        ]

        assert (
            "品种 Variety" in embarque.columns
        ), f"La columna '品种 Variety' no se encuentra la liquidacion de {liquidacion}"
        column_with_total = embarque["品种 Variety"].copy().dropna()
        summarry_location = column_with_total[
            column_with_total.str.contains("total", case=False)
        ]
        assert (
            len(summarry_location) == 1
        ), f"No se encontró el resumen en la liquidación {liquidacion}."
        summarry_location = summarry_location.index[0]

        cost_location = embarque[
            embarque.iloc[:, 0] == "其他费用 Additional Fees"
        ].index[0]

        main = embarque.iloc[: summarry_location + 1].copy().reset_index(drop=True)
        not_main = embarque.iloc[cost_location:].copy().reset_index(drop=True)

        if "总数 (美金) Total" in main.columns:
            main = main.rename(columns={"总数 (美金) Total": "总数 (美金) Total USD"})

        wanted_columns = [
            "日期 Date",
            "板号 Pallet No.",
            "果园 CSG",
            "品种 Variety",
            "大小 Size",
            "数量 Quantity",
            "规格 Specification",
            "价格 (人民币) Price RMB",
            "总数 (人民币) Total RMB",
            "总数 (美金) Total USD",
            "每箱收益  FOB FOB Return",
            "总收益 FOB Total Return",
        ]

        missing_columns = (
            set(wanted_columns)
            - set(main.columns)
            - {"每箱收益  FOB FOB Return", "总收益 FOB Total Return"}
        )
        assert (
            missing_columns == set()
        ), f"Las columnas de la tabla principal del archivo {liquidacion} no son las correctas. Deben ser {wanted_columns} pero faltan {missing_columns}."

        if not {"每箱收益  FOB FOB Return", "总收益 FOB Total Return"}.issubset(
            set(main.columns)
        ):
            main["每箱收益  FOB FOB Return"] = 0
            main["总收益 FOB Total Return"] = 0

        main = main[wanted_columns]

        main.at[main.index[-1], "品种 Variety"] = np.nan

        not_main = not_main.dropna(axis=1, how="all")

        not_main.columns = not_main.iloc[0]
        not_main = not_main.iloc[1:]

        cost_column_dict = {
            "其他费用 Additional Fees": "其他费用 Additional Fees",
            "人民币 RMB": "人民币 RMB",
            "美元 USD": "美金 USD",
        }
        not_main = not_main.rename(columns=cost_column_dict)
        cost = not_main.copy()[cost_column_dict.values()].dropna(how="all")
        note = not_main.drop(columns=cost_column_dict.values()).dropna(how="all")

        cost["其他费用 Additional Fees"] = cost["其他费用 Additional Fees"].str.replace(
            "）", ")"
        )

        embarque = [main, cost, note]
        for idx in range(len(embarque)):
            embarque[idx] = embarque[idx].reset_index(drop=True)
        embarques.append(embarque)
        paginas_list.append(1)

    return embarques, paginas_list


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

    liquidacion_list = [[main, cost, note]]

    return liquidacion_list, [1]


def interpreter_JF(liquidacion: str) -> pd.DataFrame:
    """
    Esta función tiene como objetivo ajustar el formato de la liquidacion de Jumbo Fruit (203/2024) al formato standard para luego ser usados en liquidacion_standard.

    Args:
        liquidacion (str): Ruta del archivo de liquidación.

    Returns:
        pd.DataFrame: DataFrame con el formato de liquidacion standard.

    Raises:
        AssertionError: Si el archivo de liquidación no existe, no es un archivo o no es un archivo .pdf o .xlsx.
    """
    assert os.path.exists(liquidacion), f"El archivo '{liquidacion}' no existe."
    assert os.path.isfile(liquidacion), f"El archivo '{liquidacion}' no es un archivo."
    assert liquidacion.endswith(
        (".xlsx", ".xls")
    ), f"El archivo '{liquidacion}' no es un archivo .xlsx o .xls."

    # Divide RMB by the following to obtain USD
    RMB_to_USD = 7.1892

    # Leemos el archivo
    liquidacion_df = pd.read_excel(liquidacion, dtype=str)

    # Encontramos la tabla main
    assert (
        "Date" in liquidacion_df.iloc[:, 0].values
    ), f"La tabla principal no fue encontrada en el archivo {liquidacion}: no existe la columna '{'Date'}' en la columna 1 del archivo .xlsx."
    main_location = liquidacion_df[liquidacion_df.iloc[:, 0] == "Date"].index[0]
    liquidacion_df = liquidacion_df.iloc[main_location:].reset_index(drop=True)

    # Nos aseguramos que tenga las columnas necesarias
    liquidacion_df.iloc[0] = liquidacion_df.iloc[0].apply(
        lambda x: x.title() if x != "Total（RMB）" else x
    )
    assert set(main_dict_liq_JF.keys()) == set(
        liquidacion_df.iloc[0]
    ), f"Las columnas de la tabla principal del archivo {liquidacion} no son las correctas. Deben ser {list(main_dict_liq_JF.keys())} pero son {list(liquidacion_df.iloc[0])}"

    # Create a new row with translations from the dictionary
    translation_row = liquidacion_df.iloc[0].replace(main_dict_liq_JF)

    # Insert the new row above the 'main_location'
    liquidacion_df = pd.concat(
        [translation_row.to_frame().T, liquidacion_df], ignore_index=True
    )

    # Establecemos los nombres de la columna
    liquidacion_df.columns = liquidacion_df.iloc[0]
    liquidacion_df = liquidacion_df[main_dict_liq_JF.values()]

    # Eliminamos valores negativos y los valores vacíos
    liquidacion_df["金额"] = liquidacion_df["金额"].str.replace("-", "", regex=False)
    liquidacion_df = liquidacion_df.replace("", np.nan)

    # Establecemos las observaciones como la primera columna
    liquidacion_df = liquidacion_df[
        ["观察"] + [col for col in liquidacion_df.columns if col != "观察"]
    ]

    # Creamos la columna Total (USD)
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

    # Agregamos "total" en la primera columna, en la fila donde se encuentra el total
    filtered_df = liquidacion_df[liquidacion_df["重量"].notna()].copy()
    assert any(
        filtered_df["重量"].str.contains("合计")
    ), "No se pudo encontrar el resumen: no se encontró la el elemento '合计' en la columna '重量'."
    summary_location = filtered_df[filtered_df["重量"].str.contains("合计")].index[0]
    liquidacion_df.iloc[summary_location, 0] = "total"

    # Arreglamos el formato de los customs
    liquidacion_df = liquidacion_df.replace("0", np.nan)

    # pop-eamos los costos de las liquidaciones
    cost = liquidacion_df.iloc[summary_location + 1 :].copy()
    liquidacion_df = liquidacion_df.iloc[: summary_location + 1].copy()

    # Modificamos CSG para ser vacía y coincidir con el formato standard. Eliminamos caracter chino en summary
    liquidacion_df["CSG"] = "CSG"
    liquidacion_df.loc[2:, "CSG"] = np.nan
    liquidacion_df.iloc[-1] = liquidacion_df.iloc[-1].apply(
        lambda cell: np.nan if "合计" in str(cell) else cell
    )

    # Movemos los índices dos columnas a la derecha
    assert any(
        "commission" in str(value).lower() for value in cost["尺寸"].values
    ), "No se pudo encontrar la fila de comisión: no se encontró la fila que contenga 'Commission' en la columna '尺寸'."
    cost["CSG"] = cost["尺寸"]
    cost["尺寸"] = np.nan
    cost["日期"] = cost["重量"]
    cost["重量"] = np.nan
    cost["到货数量"] = np.nan

    liquidacion_df = pd.concat([liquidacion_df, cost])

    return interpreter_standard(liquidacion_df)


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

    cost["尺寸"] = np.nan
    cost["单价"] = np.nan
    cost = cost.iloc[:-1]

    liquidacion_df = pd.concat([main, cost])
    liquidacion_df.iloc[0] = liquidacion_df.columns

    return liquidacion_df


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


def interpreter(liquidacion: str) -> tuple[list, list]:
    """
    Esta función interpreta los datos de un archivo de liquidación y devuelve una tupla con las siguientes coordenadas:

    0) Lista de listas con la informacion de la liquidación.
    1) Lista de enteros con las páginas de la liquidación.

    Args:
        liquidacion (str): Ruta del archivo de liquidación.

    Returns:
        list: Lista de listas con los datos de la liquidación.

    Raises:
        AssertionError: Si el archivo de liquidación no existe, no es un archivo o no es un archivo .pdf o .xlsx.
    """
    assert os.path.exists(liquidacion), f"El archivo '{liquidacion}' no existe."
    assert os.path.isfile(liquidacion), f"El archivo '{liquidacion}' no es un archivo."
    assert liquidacion.endswith(
        (".pdf", ".xlsx", ".xls")
    ), f"El archivo '{liquidacion}' no es un archivo .pdf o .xlsx."

    filename = filename = os.path.basename(liquidacion)

    assert (
        filename.startswith("HT")
        or filename.startswith("8F")
        or filename.startswith("HFF")
        or filename.startswith("BQ")
    ), f"No se pudo detectar el formato del archivo {filename}, asegurece que empiece con alguno de los siguientes: 'HT', '8F', 'HFF', 'BQ'."

    # Verificamos el tipo de liquidación
    if filename.startswith("HT"):
        liquidacion_list = interpreter_12Islands(liquidacion)
    elif filename.startswith("8F"):
        liquidacion_list = interpreter_standard(liquidacion)
    elif filename.startswith("BQ"):
        liquidacion_list = interpreter_JF(liquidacion)
    elif filename.startswith("HFF"):
        if filename[4:].startswith("SEA"):
            liquidacion = interpreter_HFF_SEA(liquidacion)
        liquidacion_list = interpreter_HFF(liquidacion)

    return liquidacion_list


if __name__ == "__main__":
    embarque_example1, page_example1 = interpreter(example1)
    print("Example1:")
    print("Main:")
    print(embarque_example1[0][0])
    print("Cost:")
    print(embarque_example1[0][1])
    print("Note:")
    print(embarque_example1[0][2])
    print()

    embarque_example2, page_example2 = interpreter(example2)
    print("Example2:")
    print("Main:")
    print(embarque_example2[0][0])
    print("Cost:")
    print(embarque_example2[0][1])
    print("Note:")
    print(embarque_example2[0][2])
    print()
