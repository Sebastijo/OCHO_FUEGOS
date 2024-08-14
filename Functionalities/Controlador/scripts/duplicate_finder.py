"""
Encontrar los elementos duplicados basado en el key utilizado para el merge del pseudocontrol con las liquidaciones
"""

# Importamos paquetes
import pandas as pd

# Importamos modulos propios
from src.backend.embarques import pseudoControl
from src.config import variables as var

# Variables globales
key_liq = var.key_liq

# Paths
embarque_path = r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\base_embarques.xlsx"
facturas_path = r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\facturas_proformas.xlsx"
tarifas_path = r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\tarifa_aerea.xlsx"
download_path = r"C:\Users\spinc\Desktop\embarques_duplicados.xlsx"

# Obtenemos el pseudocontrol y obtenemos los duplicados en un archivo Excel.
pseudo_control = pseudoControl(embarque_path, facturas_path, tarifas_path)
duplicates = pseudo_control[pseudo_control.duplicated(subset=key_liq, keep=False)]
duplicates.to_excel(download_path, index=False, engine="openpyxl")
