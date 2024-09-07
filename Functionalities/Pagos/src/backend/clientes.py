"""
El objetivo de este modulo es crear funciones que permtan
que el usuario modifique los clientes de la fucionalidad de pagos.
"""

# Importamos las librerias necesarias
from pathlib import Path

from src.config.universal_variables import pagos_dir
from src.backend.control_de_pagos import control_de_pagos_path  
from src.backend.boleta import embarques_path, contratos_path

clientes_path = pagos_dir / "clientes.csv"

# Leemos el archivo de clientes de existir
def update_clients() -> list[str]:
    
    embarques = pd.read_excel(embarques_path)
    contratos = pd.read_excel(contratos_path)

    clientes = list(set(embarques["RecieverName"].to_list() + contratos["Cliente"].to_list()))

    return clientes

