"""
El objetivo de este archivo es crear versiones mock de los archivos de entrada
"""

import pandas as pd
import os
from src.config import variables as var

embarquesDict = var.embarquesDict
facturasDict = var.facturasDict
tarifaDict = var.tarifaDict

# Paths to your input files
embarques_path_ = (
    r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\base_embarques.xlsx"
)
facturas_path_ = (
    r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\facturas_proformas.xlsx"
)
tarifa_path_ = r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\tarifa_aerea.xlsx"

mock_embarque_path = r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\mock_base_embarques.xlsx"
mock_facturas_path = r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\mock_facturas_proformas.xlsx"
mock_tarifa_path = r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\mock_tarifa_aerea.xlsx"

liquidaciones_path_ = r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\Liquidaciones\All 8F Sales Summary (1).pdf"

mock_liquidaciones_path = r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\mock_liquidaciones\All 8F Sales Summary (1).pdf"

if not os.path.exists(mock_embarque_path):
    # Extraemos las primeras 5 filas de embarques.
    embarques_df = pd.read_excel(embarques_path_, engine="openpyxl", dtype = str)
    embarques_df = embarques_df.iloc[:5, :]
    embarques_df = embarques_df[list(embarquesDict.keys())]
    # Transformamos el embarque a un Excel
    embarques_df.to_excel(mock_embarque_path, index=False)

if not os.path.exists(mock_facturas_path):
    # Extraemos las primeras 5 filas de facturas.
    facturas_df = pd.read_excel(facturas_path_, engine="openpyxl", dtype = str)
    facturas_df = facturas_df.iloc[:5, :]
    facturas_df = facturas_df[list(facturasDict.keys())]
    # Transformamos el embarque a un Excel
    facturas_df.to_excel(mock_facturas_path, index=False)

if not os.path.exists(mock_tarifa_path):
    # Extraemos las primeras 5 filas de tarifas.
    tarifa_df = pd.read_excel(tarifa_path_, engine="openpyxl", dtype = str)
    tarifa_df = tarifa_df.iloc[:5, :]
    tarifa_df = tarifa_df[list(tarifaDict.keys())]
    # Transformamos el embarque a un Excel
    tarifa_df.to_excel(mock_tarifa_path, index=False)

# Convertimos la primera pàgina de liquidacioenes de PDF a xls.
if not os.path.exists(mock_liquidaciones_path):
    os.system(
        f"pdf2txt.py -o {mock_liquidaciones_path} -t xml -p 1 {liquidaciones_path_}"
    )