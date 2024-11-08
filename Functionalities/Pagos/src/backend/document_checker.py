"""
This module's objective is to check if the document is in a valid format.
"""

import pandas as pd
from pathlib import Path

from src.config.universal_variables import (
    pagos_dir,
    embarque_path_pointer,
    contratos_path_pointer,
    get_pointer_path,
)

boleta_path = pagos_dir / "boleta.csv"
control_de_pagos_path = pagos_dir / "control_de_pagos.csv"

embarques_path = get_pointer_path(embarque_path_pointer, "base de embarques")
contratos_path = get_pointer_path(contratos_path_pointer, "base de contratos")

def check_document()

    try:
        boleta: pd.DataFrame = pd.read_csv(boleta_path)
    except FileNotFoundError:
        ERROR = "No se pudo cargar el archivo ubicado en: " + str(boleta_path) + ". Asegurese de que el archivo sea un archivo CSV."
        return ERROR
    
    try:
        control_de_pagos: pd.DataFrame = pd.read_csv(control_de_pagos_path)
    except FileNotFoundError:
        ERROR = "No se pudo cargar el archivo ubicado en: " + str(control_de_pagos_path) + ". Asegurese de que el archivo sea un archivo CSV."
        return ERROR
    
    try:
        embarques: pd.DataFrame = pd.read_excel(
        embarques_path,
        usecols=[
            "PalletRowId",
            "ReceiverName",
            "CaliberName",
            "PackageNetWeight",
            "Quantity",
        ],
    )
    except FileNotFoundError:
        ERROR = "No se pudo cargar el archivo ubicado en: " + str(embarques_path) + ". Asegurese de que el archivo sea un archivo Excel" + " y que contenga las columnas: PalletRowId, ReceiverName, CaliberName, PackageNetWeight, Quantity."
        return ERROR

    try:
        contratos: pd.DataFrame = pd.read_excel(contratos_path)
    except FileNotFoundError:
        ERROR = "No se pudo cargar el archivo ubicado en: " + str(contratos_path) + ". Asegurese de que el archivo sea un archivo Excel."
        return False
