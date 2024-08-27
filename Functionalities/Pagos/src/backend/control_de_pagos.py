"""
El objetivo de este modulo es agregar datos al control de pagos.
Se crea uan función que recibe los datos correspondientes a un fila de control de pagos
y los agrega a la base de datos. La inteción inicial es que esta función sea usada para
agregar datos a la base de datos desde la interfaz gráfica.
"""

# Importamos las librerias necesarias
import pandas as pd
from datetime import datetime
import tkinter as tk
from pathlib import Path

from src.config.universal_variables import pagos_dir
from ..frontend.moneyLabel import MoneyLabel

control_de_pagos_path = pagos_dir / "control_de_pagos.csv"

# Leemos el control de pagos guardado en el cache
try:
    control_de_pagos = pd.read_csv(control_de_pagos_path)
except FileNotFoundError:
    control_de_pagos_dict = {
        "Fecha Pago": [],
        "Cliente": [],
        "Pais Destino": [],
        "Ingreso": [],
        "Observaciones": [],
    }
    control_de_pagos = pd.DataFrame(control_de_pagos_dict)


def actualizar_moneyLabel(widget: MoneyLabel) -> None:
    """
    Actualiza el valoe de un `MoneyLabel` a partir de `control_de_pago`.
    """
    cliente = widget.cliente
    money = control_de_pagos[control_de_pagos["Cliente"] == cliente]["Ingreso"].sum()
    widget.set_value(money)


def agregar_pago(
    cliente: MoneyLabel,
    fecha: datetime,
    pais: str,
    ingreso: float,
    observacion: str,
    control_de_pagos: pd.DataFrame = control_de_pagos,
) -> None:
    """
    Agrega un pago al control de pagos.

    Args:
        cliente (MoneyLabel): MoneyLabel asociado a un cliente.
        fecha (datetime): Fecha del pago.
        pais (str): País de destino.
        ingreso (float): Ingreso del pago.
        observacion (str): Observaciones del pago.

    Returns:
        None

    Raises:

    """
    client_name: str = cliente.cliente
    new_row = {
        "Fecha Pago": fecha,
        "Cliente": client_name,
        "Pais Destino": pais,
        "Ingreso": ingreso,
        "Observaciones": observacion,
    }
    control_de_pagos.loc[len(control_de_pagos)] = new_row
    actualizar_moneyLabel(cliente)

    return

def save_control_de_pagos() -> None:
    """
    Guarda el control de pagos en la carpeta correspondiente.

    Args:
        save_button (Boton): Botón que llama a la función.

    Returns:
        None
    """
    control_de_pagos.to_csv(control_de_pagos_path, index=False)
    return
