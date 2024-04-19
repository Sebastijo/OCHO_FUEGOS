"""
El objetivo de este módulo es interpretar los archivos de liquidación de Jumbo Fruit (BQ) y ajustarlos al formato standard para luego ser usados en liquidacion_standard.

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
    from src.backend.interpreters.standard_interpreter import interpreter_standard
else:
    from ...config import variables as var
    from .standard_interpreter import interpreter_standard

# Definimos variables globales
main_dict_liq_standard = var.main_dict_liq_standard
main_dict_liq_JF = var.main_dict_liq_JF
main_list_liq_HFF = var.main_list_liq_HFF
main_list_liq_HFF_SEA = var.main_list_liq_HFF_SEA


def interpreter_BQ(liquidacion: str) -> pd.DataFrame:
    """
    Esta función tiene como objetivo ajustar el formato de la liquidacion de Jumbo Fruit (BQ) (203/2024) al formato standard para luego ser usados en liquidacion_standard.

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
    assert any(
        "add-value duty" in str(value).lower() for value in cost["尺寸"].values
    ), "No se pudo encontrar la fila de arancel adicional: no se encontró la fila que contenga 'Add-Value Duty' en la columna '尺寸'."
    VAT_location = cost[
        cost["尺寸"].str.contains("add-value duty", case=False, na=False)
    ].index[0]
    cost.at[VAT_location, "尺寸"] = "VAT"
    cost["CSG"] = cost["尺寸"]
    cost["尺寸"] = np.nan
    cost["日期"] = cost["重量"]
    cost["重量"] = np.nan
    cost["到货数量"] = np.nan

    liquidacion_df = pd.concat([liquidacion_df, cost])

    return interpreter_standard(liquidacion_df)
