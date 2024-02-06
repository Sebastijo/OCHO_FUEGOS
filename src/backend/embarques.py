"""
El objetivo de este modulo es tomar tres archivos: embarques, tarifa y factura para agregar la información pertinente a un archivo de control de embarques.
Este documento contine todo el proceso de ventas que no incluye la información de las liquidaciones.
Empresa: Ocho Fuegos
Autor: Sebastián P. Pincheira
Fecha: 10/01/2024
Lenguaje: Python 3.11.7
Librerías:
- pandas: 2.2.0
"""

# Importamos paquetes
import pandas as pd
from datetime import datetime
import os


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
cherry_color = var.cherry_color
COD_PUERTO_EMBARQUE = var.COD_PUERTO_EMBARQUE
COD_PUERTO_DESTINO = var.COD_PUERTO_DESTINO


if __name__ == "__main__":
    # Paths to your input files
    embarques_path_ = (
        r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\base_embarques.xlsx"
    )
    facturas_path_ = (
        r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\facturas_proformas.xlsx"
    )
    tarifa_path_ = r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\tarifa_aerea.xlsx"

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
    embarques_path: str, facturas_path: str, tarifa_path: str
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Function to be called in pseudoControl with the objective of importing and cheking the validity of the inputted Excel files
    Returns a tuple with the following coordinates:

    0) embarques: pd.DataFrame
    1) facturas: pd.DataFrame
    2) tarifa: pd.DataFrame

    Args:
        embarques_path (str): Path to the embarques Excel file.
        facturas_path (str): Path to the facturas Excel file.
        tarifa_path (str): Path to the tarifa Excel file.

    Returns:
        tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, str]: Tuple with the dataframes and an error message.
    """
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
            facturas = pd.read_excel(facturas_path, sheet_name="BillsRows", dtype=str)
            tarifa = pd.read_excel(tarifa_path, sheet_name="Instructives", dtype=str)
    except Exception as e:
        raise ValueError(
            f"No se pudo imporat alguno dos los siguientes: base embarques, facturas, tarifas. El error encontrado es: {e}"
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

    return embarques, facturas, tarifa


def pseudoControl(
    embarques_path: str, facturas_path: str, tarifa_path: str
) -> pd.DataFrame:
    """
    Esta función toma tres archivos: embarques, tarifa y factura para agregar la información pertinente a un archivo de control de embarques.

    Args:
        embarques_path (str): Path del archivo de embarques.
        facturas_path (str): Path del archivo de facturas.
        tarifa_path (str): Path del archivo de tarifa.

    Returns:
        pd.DataFrame: Dataframe de control de embarques.
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

    # importamos y revisamos los archivos
    embarques, facturas, tarifa = import_and_check(
        embarques_path, facturas_path, tarifa_path
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

    # Agregamos los Freight Costs a embarques
    embarques = pd.merge(embarques, tarifa, on="INSTRUCTIVO", how="left")

    # Definimos las keys de los dataframes
    embarques["key"] = embarques.apply(lambda row: tuple(row[key_columns]), axis=1)
    facturas["key"] = facturas.apply(lambda row: tuple(row[key_columns]), axis=1)

    # Eliminamos las columnas que no son necesarias de facturas
    facturas = facturas[["FACT PROFORMA $/CAJA", "TC Factura", "key"]]

    # Definimos el dataframe final "control"
    control = pd.merge(embarques, facturas, on="key", how="left")

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
    control["CAJAS"] = pd.to_numeric(control["CAJAS"], errors="coerce")

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
        "FLETE/kg",
    ]

    control = control[column_order]

    return control


if __name__ == "__main__":
    control, errores = pseudoControl(embarques_path_, facturas_path_, tarifa_path_)

    print("Control de embarques (sin liquidaciones):")
    print(control)
    print(errores)

    print("Observación:", "Falta la parte en rojo en la referencia")
