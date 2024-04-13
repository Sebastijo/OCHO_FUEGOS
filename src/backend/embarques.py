"""
El objetivo de este modulo es tomar tres archivos: embarques, tarifa y factura para agregar la información pertinente a un archivo de control de embarques.
Este documento contine todo el proceso de ventas que no incluye la información de las liquidaciones.
Empresa: Ocho Fuegos
Autor: Sebastián P. Pincheira
Fecha: 10/01/2024
Lenguaje: Python 3.11.7
Librerías:
- pandas: 2.2.0
- sympy: 1.12
- numpy: 1.26.3
"""

# Importamos paquetes
import pandas as pd
import sympy as sp
import numpy as np
from datetime import datetime
import os
import json
import sys


# Definimos la fecha actual
fecha_actual = datetime.now().date()

# Modulos propios
if __name__ == "__main__":
    from src.config import variables as var
else:
    from ..config import variables as var

# Variables globales
embarquesDict = var.embarquesDict
facturasDict = var.facturasDict
tarifaDict = var.tarifaDict
key_columns = var.key_columns
key_precios_contrato = var.key_precios_contrato
cherry_color = var.cherry_color
COD_PUERTO_EMBARQUE = var.COD_PUERTO_EMBARQUE
key_liq = var.key_liq
key_liq_incompleto = var.key_liq_incompleto
formatos_con_CSG = var.formatos_con_CSG
directory = var.directory

# Cargamos el codigo de puerto destino actualizado
datos_folder = os.path.join(directory, "Datos del programa")
variables_folder = os.path.join(datos_folder, "Variables")
with open(os.path.join(variables_folder, "cod_puerto_destino.json"), "r") as file:
    COD_PUERTO_DESTINO_configuracion = json.load(file)
COD_PUERTO_DESTINO = COD_PUERTO_DESTINO_configuracion


if __name__ == "__main__":
    # Paths to your input files
    embarques_path_ = (
        r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\Base embarques.xlsx"
    )
    facturas_path_ = (
        r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\Facturas proformas.xlsx"
    )
    tarifa_path_ = r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\Tarifas.xlsx"

    # Pickle files for each DataFrame
    embarques_pickle = (
        r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\pickles\embarques_dataframe.pkl"
    )
    facturas_pickle = (
        r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\pickles\facturas_dataframe.pkl"
    )
    tarifa_pickle = (
        r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\pickles\tarifa_dataframe.pkl"
    )


def import_and_check(
    embarques_path: str,
    facturas_path: str,
    tarifa_path: str,
    update_loading_bar: callable = None,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Function to be called in pseudoControl with the objective of importing and cheking the validity of the inputted Excel files
    Returns a tuple with the following coordinates:

    0) embarques: pd.DataFrame
    1) facturas: pd.DataFrame
    2) tarifa: pd.DataFrame
    3) precios_contrato: pd.DataFrame
    4) flete_real: pd.DataFrame
    5) costo_seco: pd.DataFrame

    Args:
        embarques_path (str): Path to the embarques Excel file.
        facturas_path (str): Path to the facturas Excel file.
        tarifa_path (str): Path to the tarifa Excel file.
        update_loading_bar (callable, optional): Function to update the loading bar. Defaults to None.

    Returns:
        tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]: Tuple with the dataframes.
    """

    precios_contrato_path = os.path.join(variables_folder, "precios_contrato.xlsx")
    flete_real_path = os.path.join(variables_folder, "flete_real.xlsx")
    costo_seco_path = os.path.join(variables_folder, "costo_seco.xlsx")
    try:
        if (
            __name__ == "__main__"
            and embarques_path == embarques_path_
            and facturas_path == facturas_path_
            and tarifa_path == tarifa_path_
        ):
            # Load or create and save pickled files
            if os.path.exists(embarques_pickle):
                embarques = pd.read_pickle(embarques_pickle)
            else:
                embarques = pd.read_excel(embarques_path, sheet_name="Hoja1", dtype=str)
                embarques.to_pickle(embarques_pickle)

            if os.path.exists(facturas_pickle):
                facturas = pd.read_pickle(facturas_pickle)
            else:
                facturas = pd.read_excel(
                    facturas_path, sheet_name="BillsRows", dtype=str
                )
                facturas.to_pickle(facturas_pickle)

            if os.path.exists(tarifa_pickle):
                tarifa = pd.read_pickle(tarifa_pickle)
            else:
                tarifa = pd.read_excel(
                    tarifa_path, sheet_name="Instructives", dtype=str
                )
                tarifa.to_pickle(tarifa_pickle)

        else:
            embarques = pd.read_excel(embarques_path, sheet_name="Hoja1", dtype=str)
            if update_loading_bar:  # 2ra operacion
                update_loading_bar()
            facturas = pd.read_excel(facturas_path, sheet_name="BillsRows", dtype=str)
            if update_loading_bar:  # 3ra operacion
                update_loading_bar()
            tarifa = pd.read_excel(tarifa_path, sheet_name="Instructives", dtype=str)
            if update_loading_bar:  # 4ra operacion
                update_loading_bar()
        precios_contrato = pd.read_excel(precios_contrato_path, dtype=str)
        flete_real = pd.read_excel(flete_real_path, dtype=str)
        costo_seco = pd.read_excel(costo_seco_path, dtype=str)
        if update_loading_bar:  # 5ta operacion
            update_loading_bar()

    except Exception as e:
        raise ValueError(
            f"No se pudo imporat alguno dos los siguientes: base embarques, facturas, tarifas, precios_contrato, flete_real, costo_seco. El error encontrado es: {e}"
        )

    # Revisamos las columnas de embarques
    embarques_difference = set(embarquesDict.keys()) - set(embarques.columns)
    assert (
        embarques_difference == set()
    ), f"La(s) columna(s) {embarques_difference} no se encuentra(n) en el archivo de base embarques."

    # Revisamos las columnas de facturas
    facturas_difference = set(facturasDict.keys()) - set(facturas.columns)
    assert (
        facturas_difference == set()
    ), f"La(s) columna(s) {facturas_difference} no se encuentra(n) en el archivo de facturas."

    # Revisamos las columnas de tarifa
    tarifa_difference = set(tarifaDict.keys()) - set(tarifa.columns)
    assert (
        tarifa_difference == set()
    ), f"La(s) columna(s) {tarifa_difference} no se encuentra(n) en el archivo de tarifa."

    # Revisamos las columnas de precios_contrato
    precios_contrato_difference = {
        "CALIBRES",
        "KG NET/CAJA",
        "ETD WEEK",
        "CLIENTE",
        "PRECIO CONTRATO $/CAJA",
    } - set(precios_contrato.columns)
    assert (
        precios_contrato_difference == set()
    ), f"La(s) columna(s) {precios_contrato_difference} no se encuentra(n) en el archivo de precios_contrato."

    # Revisamos las columnas de flete_real
    flete_real_difference = {
        "AWB - BL",
        "BRUTOS DOCS",
        "FLETE AWB",
        "GASTOS LOCALES PESOS",
        "GASTOS LOCALES DOLARES",
    } - set(flete_real.columns)
    assert (
        flete_real_difference == set()
    ), f"La(s) columna(s) {flete_real_difference} no se encuentra(n) en el archivo de flete_real."

    # Revisamos las columnas de costo_seco
    costo_seco_difference = {
        "TIPO DE EMBARQUE",
        "KG NET/CAJA",
        "COSTO SECO/KG",
    } - set(costo_seco.columns)
    assert (
        costo_seco_difference == set()
    ), f"La(s) columna(s) {costo_seco_difference} no se encuentra(n) en el archivo de costo_seco."

    return embarques, facturas, tarifa, precios_contrato, flete_real, costo_seco


def simplifier(pseudocontrol: pd.DataFrame) -> pd.DataFrame:
    """
    Recibe un (DataFrame del tipo entregado por la función) pseudoControl y devuelve el DataFrame con los siguientes cambios:
    - Deja un único elemento por cada key_liq (elimina los duplicados).
    - El representante de cada key_liq, en cada feature donde haya habido una diferencia entre los duplicados, se convierte a una tupla con el valor de la columna de cada representante.
    - La cantidad de cajas, "CAJAS", siempre es una tupla con la cantidad de cajas de cada representante.
    - Se agrega una columna a la derecha de "CAJAS", "CAJAS TOTALES", con la suma de las cajas de cada representante.

    Args:
        df (pd.DataFrame): DataFrame del tipo entregado por la función pseudoControl.

    Returns:
        pd.DataFrame: DataFrame con los cambios especificados.

    Raises:
        AssertionError: Si el input no es un DataFrame.
    """
    assert isinstance(
        pseudocontrol, pd.DataFrame
    ), f"El input '{pseudocontrol}' no es un DataFrame. En la función 'simplifier'. No se pudieron unir los pallets repetidos."

    def unioner(df):
        """
        Recibe un DataFrame y lo reduce a un solo representante (fila). Si hay diferencias entre los representantes, estas se convierten a tuplas.
        Si existe una columna con el nombre "CAJAS", la columna siempre se convierte en una tupla con la canidad de cajas de cada representante.
        """
        simp_df_data = {}
        # Reducimos todas las filas a una sola fila, con cada elemento, de haber diferencias o ser CAJAS, convertido a una tupla.
        for column in df.columns:
            value = tuple(df[column].tolist())
            value = tuple(
                None if isinstance(x, (int, float)) and np.isnan(x) else x
                for x in value
            )
            columnas_cuantitativas = {
                "CAJAS",
                "PALLETS",
                "NETOS",
                "BRUTOS",
                "FACT PROFORMA $ TOTAL",
                "PRECIO CONTRATO",
                "BRUTOS_2",
                "FLETE_TOTAL",
                "GASTOS LOCALES CLP",
                "GASTOS LOCALES USD",
                "FLETE TOTAL 2",
            }
            if (
                (
                    (not column in columnas_cuantitativas)
                    and all(elem == value[0] for elem in value)
                )
                or len(value) == 1
                or all(x is np.nan for x in value)
            ):
                value = value[0]
            simp_df_data[column] = [value]
        simp_df = pd.DataFrame(simp_df_data)

        return simp_df

    # Reducimos el DataFrame a un solo representante por key_liq y key_liq_incompleto, según corresponda
    # Harvest Time (Alex) es el único que usa el key_liq
    pseudocontrol_HT = pseudocontrol[pseudocontrol["CLIENTE"].isin(formatos_con_CSG)]
    pseudocontrol_not_HT = pseudocontrol[
        ~pseudocontrol["CLIENTE"].isin(formatos_con_CSG)
    ]

    pseudocontrol_HT = (
        pseudocontrol_HT.groupby(key_liq).apply(unioner).reset_index(drop=True)
    )
    pseudocontrol_not_HT = (
        pseudocontrol_not_HT.groupby(key_liq_incompleto)
        .apply(unioner)
        .reset_index(drop=True)
    )

    pseudocontrol = pd.concat([pseudocontrol_HT, pseudocontrol_not_HT])

    # SUMAMOS TUPLAS DECEADAS: CAJAS SUMADAS, FACT PROFORMA $ TOTAL SUMADAS, PRECIO CONTRATO SUMADAS
    def sumador_de_tuplas(cell):
        if isinstance(cell, tuple):
            cell = tuple(0 if pd.isna(x) else x for x in cell)
            return sum(cell)
        else:
            return cell

    columnas_por_sumar = [
        "CAJAS",
        "FACT PROFORMA $ TOTAL",
        "PRECIO CONTRATO",
        "BRUTOS_2",
        "FLETE TOTAL",
        "GASTOS LOCALES CLP",
        "GASTOS LOCALES USD",
        "FLETE TOTAL 2",
    ]
    for columna in columnas_por_sumar:
        pseudocontrol[columna] = pseudocontrol[columna].apply(sumador_de_tuplas)

    columnas_por_caja = [
        "FACT PROFORMA $/CAJA",
        "PRECIO CONTRATO $/CAJA",
        "BRUTOS_2/CJ",
        "FLETE TOTAL/CJ",
        "GASTOS LOCALES CLP/CJ",
        "GASTOS LOCALES USD/CJ",
        "FLETE TOTAL 2/CJ",
    ]

    columnas_globales = [
        "FACT PROFORMA $ TOTAL",
        "PRECIO CONTRATO",
        "BRUTOS_2",
        "FLETE TOTAL",
        "GASTOS LOCALES CLP",
        "GASTOS LOCALES USD",
        "FLETE TOTAL 2",
    ]

    for column_cj, column_gl in zip(columnas_por_caja, columnas_globales):
        pseudocontrol[column_cj] = pseudocontrol[column_gl] / pseudocontrol["CAJAS"]

    return pseudocontrol


def pseudoControl(
    embarques_path: str,
    facturas_path: str,
    tarifa_path: str,
    update_loading_bar: callable = None,
) -> pd.DataFrame:
    """
    Esta función toma tres archivos: embarques, tarifa y factura para agregar la información pertinente a un archivo de control de embarques.

    Args:
        embarques_path (str): Path del archivo de embarques.
        facturas_path (str): Path del archivo de facturas.
        tarifa_path (str): Path del archivo de tarifa.

    Returns:
        pd.DataFrame: DataFrame con la información de los embarques, facturas y tarifa en un formato simplificado: un solo representante por key_liq.
    """

    for file_path in [embarques_path, facturas_path, tarifa_path]:
        assert (
            type(file_path) == str
        ), f"La ruta del archivo '{file_path}' no es una cadena de texto."
        assert os.path.exists(
            file_path
        ), f"La ruta del archivo '{file_path}' no existe."
        assert os.path.isfile(
            file_path
        ), f"'{file_path}' no es un archivo; puede que sea una carpeta."

    def simplify_decimal(x: float) -> str:
        """
        Formato para la columna KG NET/CAJA
        """
        if isinstance(x, str):
            # Extract the expression from the string
            expression = x.split("KG")[0]
            # Simplify the expression
            simplified = sp.simplify(expression)
            # Remove unnecessary decimal places
            simplified = (
                str(simplified).rstrip("0").rstrip(".")
                if "." in str(simplified)
                else str(simplified)
            )
            # Return the simplified expression
            return simplified
        elif isinstance(x, (int, float)):
            simplified = str(x).rstrip("0").rstrip(".") if "." in str(x) else str(x)
            return simplified
        else:
            return np.nan if np.isnan(x) else str(x)

    # importamos y revisamos los archivos
    embarques, facturas, tarifa, precios_contrato, flete_real, costo_seco = (
        import_and_check(
            embarques_path,
            facturas_path,
            tarifa_path,
            update_loading_bar,
        )
    )

    # Traducimos
    embarques.rename(
        columns=embarquesDict,
        inplace=True,
    )
    facturas.rename(columns=facturasDict, inplace=True)
    tarifa.rename(columns=tarifaDict, inplace=True)

    # Extraemos las columnas a utilizar en los dataframes
    embarques = embarques[list(embarquesDict.values())]
    facturas = facturas[list(facturasDict.values())]
    tarifa = tarifa[list(tarifaDict.values())]
    precios_contrato = precios_contrato[
        ["CALIBRES", "KG NET/CAJA", "ETD WEEK", "CLIENTE", "PRECIO CONTRATO $/CAJA"]
    ]
    flete_real = flete_real[
        [
            "AWB - BL",
            "BRUTOS DOCS",
            "FLETE AWB",
            "GASTOS LOCALES PESOS",
            "GASTOS LOCALES DOLARES",
        ]
    ]
    costo_seco = costo_seco[["TIPO DE EMBARQUE", "KG NET/CAJA", "COSTO SECO/KG"]]

    # Agregamos los Freight Costs a embarques
    embarques = pd.merge(embarques, tarifa, on="INSTRUCTIVO", how="left")

    # Definimos las keys de los dataframes
    embarques["key"] = embarques.apply(lambda row: tuple(row[key_columns]), axis=1)
    facturas["key"] = facturas.apply(lambda row: tuple(row[key_columns]), axis=1)

    # Eliminamos las columnas que no son necesarias de facturas
    facturas = facturas[["FACT PROFORMA $/CAJA", "TC Factura", "key"]]

    # Definimos el dataframe final "control"
    control = pd.merge(embarques, facturas, on="key", how="left")

    # Agregamos los precios de contrato al dataframe de control. Esto agrega la columna "PRECIO CONTRATO $/CAJA"
    precios_contrato["KG NET/CAJA"] = precios_contrato["KG NET/CAJA"].apply(
        simplify_decimal
    )

    control = pd.merge(control, precios_contrato, on=key_precios_contrato, how="left")

    # Agregamos los datos de flete real
    columnas_por_crear_flete_real = [
        "BRUTOS_2",
        "FLETE TOTAL",
        "GASTOS LOCALES CLP",
        "GASTOS LOCALES USD",
    ]
    source_columns_flete_real = [
        "BRUTOS DOCS",
        "FLETE AWB",
        "GASTOS LOCALES PESOS",
        "GASTOS LOCALES DOLARES",
    ]

    # Transformamos las columna necesarias a number
    for column in source_columns_flete_real:
        flete_real[column] = pd.to_numeric(flete_real[column], errors="coerce")
    for column in {"NETOS", "CAJAS"}:
        control[column] = pd.to_numeric(control[column], errors="coerce")

    # Las columnas agregadas a continuación, serán borradas eventualmetne
    control["KG_netos_BL"] = control.groupby("AWB - BL")["NETOS"].transform("sum")
    control = control.merge(flete_real, on="AWB - BL", how="left")

    # Calculamos las columnas necesarias
    for column, column_source in zip(
        columnas_por_crear_flete_real, source_columns_flete_real
    ):
        control[column] = (control[column_source] / control["KG_netos_BL"]) * control[
            "NETOS"
        ]
        control[column + "/CJ"] = control[column] / control["CAJAS"]

    control["FLETE TOTAL 2"] = control["FLETE TOTAL"] + control["GASTOS LOCALES USD"]
    control["FLETE TOTAL 2/CJ"] = control["FLETE TOTAL 2"] / control["CAJAS"]

    # Eliminamos las columnas innecesarias
    control.drop(columns=["KG_netos_BL", *source_columns_flete_real], inplace=True)

    # Agregamos los datos de costo seco
    costo_seco["KG NET/CAJA"] = costo_seco["KG NET/CAJA"].apply(simplify_decimal)
    control = pd.merge(
        control, costo_seco, on=["TIPO DE EMBARQUE", "KG NET/CAJA"], how="left"
    )

    # Calculamos el PRECIO CONTRATO
    control["PRECIO CONTRATO $/CAJA"] = pd.to_numeric(
        control["PRECIO CONTRATO $/CAJA"], errors="coerce"
    )
    control["CAJAS"] = pd.to_numeric(control["CAJAS"], errors="coerce")
    control["PRECIO CONTRATO"] = control["PRECIO CONTRATO $/CAJA"] * control["CAJAS"]

    # Parse the columns
    date_columns = [
        "FECHA FACTURA",
        "FECHA DESPACHO PLANTA",
        "FECHA EMBALAJE",
        "ETD",
        "ETA",
        "ETA REAL",
    ]

    control[date_columns] = control[date_columns].apply(pd.to_datetime)
    # control[date_columns] = pd.to_datetime(control[date_columns], errors="coerce")
    control["FACT PROFORMA $/CAJA"] = pd.to_numeric(
        control["FACT PROFORMA $/CAJA"], errors="coerce"
    )

    # Agregamos las columnas que faltan
    control["TRANSPORTE PUERTO"] = None  # Columna vacía

    control["COLOR"] = control["CALIBRES"].map(
        cherry_color
    )  # Definimos el color a partir del calibre y el dccionario cherry_color

    control["COD PUERTO EMBARQUE"] = control["PUERTO EMBARQUE"].map(
        COD_PUERTO_EMBARQUE
    )  # Conseguimos el codigo de puerto embarque a partir del puerto embarque y el diccionario COD_PUERTO_EMBARQUE

    control["COD PUERTO DESTINO"] = control["PUERTO DESTINO"].map(
        COD_PUERTO_DESTINO
    )  # Conseguimos el codigo de puerto destino a partir del puerto destino y el diccionario COD_PUERTO_DESTINO

    control["ETD REAL"] = control[
        "ETD"
    ]  # Definimos el tiempo estimado de despaco real a partir del tiempo estimado de despacho (ETD)

    control["DIAS TRANSITO"] = (
        control["ETA REAL"] - control["ETD REAL"]
    ).dt.days  # Calculamos los días transcurridos mediante tiempo final menos tiempo inicial

    control["ESTATUS EMBARQUE"] = control["ETA REAL"].apply(
        lambda x: (
            "ARRIBADO" if pd.notna(x) and x.date() < fecha_actual else "EN TRANSITO"
        )
    )  # Definimos el estatus del embarque (ARRIBADO o EN TRANSITO)

    control["RECLAMADO"] = None  # Columan vacía

    control["COMENTARIOS"] = None  # Columna vacía

    control["FECHA VENC IVV"] = None  # Columna vacía

    control["FACT PROFORMA $ TOTAL"] = (
        control["FACT PROFORMA $/CAJA"] * control["CAJAS"]
    )  # Calculamos el total de la factura proforma

    control["FACT EXPORTACION $/CAJA"] = None  # Columna vacía

    control["FACT EXPORTACION $ TOTAL"] = None  # Columna vacía

    # BillBL v.s. AWB - BL

    # Definimos el orden de las columans a mostrar en el output
    column_order = [
        "ETD WEEK",
        "EXPORTADOR",
        "INSTRUCTIVO",
        "CLIENTE",
        "CONSIGNATARIO",
        "FACTURA PROFORMA",
        "FECHA FACTURA",
        "TC Factura",
        "MODALIDAD DE VENTA",
        "INCOTERM",
        "PACKING",
        "GUIA DESPACHO",
        "FECHA DESPACHO PLANTA",
        "TRANSPORTE PUERTO",  # Empty
        "PRODUCTOR",
        "CSG",
        "FECHA EMBALAJE",
        "FOLIO",
        "ESPECIE",
        "VARIEDAD",
        "CALIBRES",
        "COLOR",
        "CODIGO EMBALAJE",
        "KG NET/CAJA",
        "BRUTOS/CAJA",
        "CAJAS",
        "PALLETS",
        "NETOS",
        "BRUTOS",
        "TIPO DE EMBARQUE",
        "NAVE",
        "PUERTO EMBARQUE",
        "COD PUERTO EMBARQUE",
        "MERCADO",
        "PAIS DESTINO",
        "PUERTO DESTINO",
        "COD PUERTO DESTINO",
        "AWB - BL",
        "VOYAGE NUMBER",
        "BOOKING",
        "CONTENEDOR",
        "LINEA AEREA/NAVIERA",
        "EMBARCADOR",
        "ETD",
        "ETA",
        "DUS",
        "SPS",
        "ETD REAL",
        "ETA REAL",
        "DIAS TRANSITO",
        "ESTATUS EMBARQUE",
        "RECLAMADO",  # Empty
        "COMENTARIOS",  # Empty
        "FECHA VENC IVV",  # Empty
        "FACT PROFORMA $/CAJA",
        "FACT PROFORMA $ TOTAL",
        "FACT EXPORTACION $/CAJA",
        "FACT EXPORTACION $ TOTAL",
        "PRECIO CONTRATO $/CAJA",
        "PRECIO CONTRATO",
        "FLETE/kg",
        "BRUTOS_2",
        "BRUTOS_2/CJ",
        "FLETE TOTAL",
        "FLETE TOTAL/CJ",
        "GASTOS LOCALES CLP",
        "GASTOS LOCALES CLP/CJ",
        "GASTOS LOCALES USD",
        "GASTOS LOCALES USD/CJ",
        "FLETE TOTAL 2",
        "FLETE TOTAL 2/CJ",
        "COSTO SECO/KG",
    ]

    # Solo mayusculas en los valores de las columnas key para liquidaciones (y en formato str)
    for key in key_liq:
        control[key] = control[key].astype(str).str.upper()

    # Simplificamos el DataFrame
    control = simplifier(control)

    control = control[column_order]

    return control


if __name__ == "__main__":
    control = pseudoControl(embarques_path_, facturas_path_, tarifa_path_)

    print("Control de embarques (sin liquidaciones):")
    print(control)