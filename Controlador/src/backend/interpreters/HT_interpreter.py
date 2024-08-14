"""
El objetivo de este módulo es definir la función interpreter_12Islands que interpreta los archivos de liquidación de 12Islands
 y los ajusta al formato standard para luego ser usados en liquidacion_standard.

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
    """
    if liquidacion.endswith(".pdf"):
        embarqueNum = 0  # Índice del embarque en la lista de embarques
        i = 0  # Índice de página (pagina - 1)
        pages_left = True
        while pages_left:  # Recorremos hasta que no queden hojas
            embarque_change = False  # "El embarque cambió respecto al ciclo anterior"
            while not embarque_change:  # Mientras nos mantengamos en el mismo embarque
                
                # Las páginas del PDF contienen distintos embarques, cada embarque puede estar contenido en varias págnas las cuales están una tras la otra.
                # Este while se encarga de identificar los diferentes embarques y poner todas las tablas de un mismo embarque en una misma msima lista metida en la lista embarques.
                
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
    """
    # else:  # Si el archivo es un excel
    embarque = pd.read_excel(liquidacion, dtype=str)
    embarque = embarque.dropna(axis=1, how="all")

    main_location = embarque[embarque.iloc[:, 0] == "日期"].index[0]
    embarque_copy = embarque.copy()
    embarque = embarque.iloc[main_location:].reset_index(drop=True)

    concatenated_string = embarque.iloc[0] + " " + embarque.iloc[1]
    embarque.columns = concatenated_string
    embarque = embarque.iloc[2:]
    embarque.reset_index(drop=True, inplace=True)
    if not "LOCALIDAD" in embarque.columns:
        total_rmb_column = embarque.columns.get_loc("总数(人民币) Total RMB")
        localidad = str(embarque_copy.iloc[main_location - 2, total_rmb_column])

    embarque.columns = [
        str(col) if not isinstance(col, float) else "nan" for col in embarque.columns
    ]

    embarque.columns = [
        column.replace(" " + " ", " ").replace("(", " (").replace("FOB FOB", " FOB FOB")
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

    cost_location = embarque[embarque.iloc[:, 0] == "其他费用 Additional Fees"].index[0]

    main = embarque.iloc[: summarry_location + 1].copy().reset_index(drop=True)
    not_main = embarque.iloc[cost_location:].copy().reset_index(drop=True)

    if not "LOCALIDAD" in main.columns:
        main["LOCALIDAD"] = localidad

    if "总数 (美金) Total" in main.columns:
        main = main.rename(columns={"总数 (美金) Total": "总数 (美金) Total USD"})

    wanted_columns = [
        "日期 Date",
        "LOCALIDAD",
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

    main["LOCALIDAD"] = main["LOCALIDAD"].replace("nan", np.nan)

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

    # Identificamos la columna VAT
    assert any(
        "vat" in str(value).lower() for value in cost["其他费用 Additional Fees"].values
    ), "No se pudo encontrar la fila de arancel adicional: no se encontró la fila que contenga 'VAT' en la columna '其他费用 Additional Fees'."
    VAT_location = cost[
        cost["其他费用 Additional Fees"].str.contains("vat", case=False, na=False)
    ].index[0]
    cost.at[VAT_location, "其他费用 Additional Fees"] = "VAT"

    embarque = [main, cost, note]
    for idx in range(len(embarque)):
        embarque[idx] = embarque[idx].reset_index(drop=True)
    embarques.append(embarque)
    paginas_list.append(1)

    return embarques, paginas_list
