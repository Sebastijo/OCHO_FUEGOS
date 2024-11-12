"""
This module's objective is to create and manage the history of the packings.
"""

import os
from pathlib import Path
from datetime import datetime
import pandas as pd

from src.config.universal_variables import (
    get_pointer_path,
    packing_history_pointer,
    history_logs_dir,
)
from .classes import Packing

today = datetime.today()

history_structure_dict: dict = {
    "FECHA": [],
    "PACKING": [],
    "MATERIAL": [],
    "CANTIDAD": [],
    "CANTIDAD PARA PEDIDO": [],
    "CANTIDAD MÁXIMA": [],
    "CANTIDAD POR PEDIR": [],
    "STOCK DE EMERGENCIA": [],
    "PEDIR MATERIAL": [],
}

history_structure: pd.DataFrame = pd.DataFrame(history_structure_dict)

paking_history_path: Path = get_pointer_path(
    packing_history_pointer, "HISTORIAL DE LOS PACKINS", create=history_structure
)

history_df: pd.DataFrame = pd.read_excel(paking_history_path)


def append_packing_history(packings: list[Packing]) -> None:
    """
    Appends the history of the packings to the history dataframe.

    Args:
        packings (list[Packing]): List of packings to append to the history.
    """
    log_path: Path = history_logs_dir / f"{today.strftime('%d-%m-%Y')}.xlsx"
    for packing in packings:
        packing.round_values()
        for material in packing:
            new_row = {
                "FECHA": today.strftime("%d-%m-%Y"),
                "PACKING": packing.name,
                "MATERIAL": material.name,
                "CANTIDAD": material.stock,
                "CANTIDAD PARA PEDIDO": material.minimum_stock,
                "CANTIDAD MÁXIMA": material.maximum_stock,
                "CANTIDAD POR PEDIR": material.order_amount,
                "STOCK DE EMERGENCIA": material.emergency_stock,
                "PEDIR MATERIAL": not material.enough_stock,
            }
            history_df.loc[len(history_df)] = new_row

    # we save to the log
    history_df.to_excel(log_path, index=False)
    # we update the history
    history_df.to_excel(paking_history_path, index=False)

    return paking_history_path
