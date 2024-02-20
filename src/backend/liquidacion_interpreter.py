"""
El objetivo de este módulo es intepretar los distintos tipos de liquidaciones que se pueden realizar en el sistema.
Los tipos de liquidaciones disponibles son:

    - 12Islands (.pdf)
    - JumboFruit (.xlsx)
    - 8F (.xlsx)

El resultado de el módulo es producir una lista de listas, cada lista representando un embarque y los elementos de la lista representadno los diversos datos presentes en un embarque.
JumboFruit y 8F usarán la misma función de interpretación, mientras que 12Islands usará una función distinta.
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
import tabula
import os
from decimal import Decimal

# importamos modulos porpios
if __name__ == "__main__":
    from src.config import variables as var
else:
    from ..config import variables as var


# Definimos variables globales
main_dict_liq_standard = var.main_dict_liq_standard

if __name__ == "__main__":
    example1 = r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\Liquidaciones\104. Liquidation-品牌-8F  柜号 SZLU-9152413.xlsx"
    example2 = r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\Liquidaciones\121. Liquidation-品牌-8F  柜号 CXRU-1465266.xlsx"


def interpreter_12Islands(liquidacion: str) -> tuple[list, list]:
    """
    Takes in a liquidación file in the forma of a PDF in the format of the 12Islands liquidation format (can have multimple embarques)
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
        ".pdf"
    ), f"El archivo en {liquidacion} no es un archivo PDF."

    embarques = []  # Lista de todos los embarques
    paginas_list = (
        []
    )  # Lista cuya n-ésima entrada contiene la primera página del n-ésimo embarque
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
    return embarques, paginas_list


def interpreter_standard(liquidacion: str) -> tuple[list, list]:
    """
    Esta función interpreta los datos de un archivo de liquidación y devuelve una tupla con las siguientes coordenadas:
    los formatos válidos de liquidaciones son: JumboFruit y 8F (standard).

    0) Lista de listas con la informacion de la liquidación.
    1) Lista de enteros con las páginas de la liquidación (en este caso, [1])

    Args:
        liquidacion (str): Ruta del archivo de liquidación.

    Returns:
        list: Lista de listas con los datos de la liquidación.

    Raises:
        AssertionError: Si el archivo de liquidación no existe, no es un archivo o no es un archivo .xlsx o .xls.
        AssertionError: Si la tabla principal no fue encontrada en el archivo de liquidación.
        AssertionError: Si las columnas de la tabla principal no son las correctas.
    """
    assert os.path.exists(liquidacion), f"El archivo '{liquidacion}' no existe."
    assert os.path.isfile(liquidacion), f"El archivo '{liquidacion}' no es un archivo."
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
            # Extract the expression from the string
            expression = x.split("KG")[0]
            # Simplify the expression
            simplified = sp.simplify(expression)
            # Convert the simplified expression to Decimal
            simplified_decimal = Decimal(str(simplified))
            # Remove unnecessary decimal places
            simplified_decimal = simplified_decimal.normalize()
            # Convert back to string
            simplified_str = str(simplified_decimal)
            # Return the simplified expression
            return f"{simplified_str}KG"
        else:
            return np.nan if np.isnan(x) else str(x)

    # Leemos el archivo
    liquidacion_df = pd.read_excel(liquidacion, dtype=str)

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
    main["日期 Date"] = main["日期 Date"].fillna("No vendido")
    main.loc[main.index[-1], "日期 Date"] = np.nan

    # Simplifacamos los pesos de las cajas (ej: 2*2.5KG -> 5KG)

    # Borramos la columna en chino
    for column in cost.columns:
        pattern = r"[^A-Za-z0-9]|(?<=\')np\.nan(?=\')"
        contains_non_american = cost[column].astype(str).str.contains(pattern, na=False)
        if contains_non_american.all():
            cost = cost.drop(columns=column)
            break
    cost.columns = ["其他费用 Additional Fees", "人民币 RMB", "美金 USD"]

    # Posicionamos donde corresponde (al final)
    assert any(
        "Commission" in value for value in cost["其他费用 Additional Fees"].values
    ), f"La fila de comisión no fue encontrada en el archivo {liquidacion}: no existe una fila que contenga '{'Commission'}' en el archivo .xlsx."
    commission_location = cost[
        cost["其他费用 Additional Fees"].str.contains("Commission")
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

    if liquidacion.endswith(".pdf"):
        liquidacion_list = interpreter_12Islands(liquidacion)
    else:
        liquidacion_list = interpreter_standard(liquidacion)

    return liquidacion_list


if __name__ == "__main__":
    embarque_example1, page_example1 = interpreter(example1)
    print("Template 8F:")
    print("Main:")
    print(embarque_example1[0][0])
    print("Cost:")
    print(embarque_example1[0][1])
    print("Note:")
    print(embarque_example1[0][2])
    print()
    embarque_example2, page_example2 = interpreter(example2)
    print("JumboFruit:")
    print("Main:")
    print(embarque_example2[0][0])
    print("Cost:")
    print(embarque_example2[0][1])
    print("Note:")
    print(embarque_example2[0][2])
    print()
