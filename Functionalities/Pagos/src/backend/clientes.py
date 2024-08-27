"""
El objetivo de este modulo es crear funciones que permtan
que el usuario modifique los clientes de la fucionalidad de pagos.
"""

# Importamos las librerias necesarias
from pathlib import Path

from src.config.universal_variables import pagos_dir

clientes_path = pagos_dir / "clientes.csv"

# Leemos el archivo de clientes de existir
def update_clients() -> list[str]:
    try:
        clientes: list[str] = clientes_path.read_text().splitlines()
    except FileNotFoundError:
        clientes = ["No hay clientes agregados"]
        # Creamos el archivo de clientes
        clientes_path.write_text("\n".join(clientes))
    return clientes

