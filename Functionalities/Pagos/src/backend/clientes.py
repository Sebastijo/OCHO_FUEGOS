"""
El objetivo de este modulo es crear funciones que permtan
que el usuario modifique los clientes de la fucionalidad de pagos.
"""

# Importamos las librerias necesarias
from pathlib import Path
import pandas as pd

from src.config.universal_variables import pagos_dir

# from .control_de_pagos import control_de_pagos_path
from .boleta import embarques_path, contratos_path


# Leemos el archivo de clientes de existir
def update_clients() -> list[str]:
    # Read only the necessary columns
    # embarques = pd.read_excel(embarques_path, usecols=["ReceiverName"])
    contratos = pd.read_excel(contratos_path, usecols=["Cliente"])

    # Get unique clients using pandas' .unique()
    # clientes = pd.concat([embarques["ReceiverName"], contratos["Cliente"]]).unique()
    clientes = contratos["Cliente"].unique()

    return sorted(clientes.tolist())


# Los clientes se obtienen de los contratos
