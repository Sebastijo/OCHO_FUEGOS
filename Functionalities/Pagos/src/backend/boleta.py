"""
El objetivo de este modulo es crear una boleta a partir de la base control y los contratos con los clientes,
la cual es guardada en un archivo csv.junto al control de pagos.Esta posteriormente será usada para descontar.
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

embarques_path = get_pointer_path(embarque_path_pointer, "base de embarques")
contratos_path = get_pointer_path(contratos_path_pointer, "base de contratos")


def actualizar_boleta() -> pd.DataFrame:
    """
    Crea una boleta a partir de la base control y los contratos con los clientes.

    Args: None

    Returns:
        pd.DataFrame: Boleta con los datos de los clientes y el precio de cada pallet.
    """
    try:
        boleta: pd.DataFrame = pd.read_csv(boleta_path
    except FileNotFoundError:
        boleta_dict: dict[str, any] = {
            "PalletRowId": [],
            "Cliente": [],
            "Precio": [],
        }
        boleta: pd.DataFrame = pd.DataFrame(boleta_dict)
        boleta.to_csv(boleta_path, index=False)

    # Importamos la base embarque quedandonos solo con los elementos que no estan en la boleta
    embarques: pd.DataFrame = pd.read_excel(embarques_path)
    embarque = embarque[~embarque["PalletRowId"].isin(boleta["PalletRowId"])]

    contratos: pd.DataFrame = pd.read_excel(contratos_path)

    # A cada elemento de embarques le asignamos un precio

    contrato_key: list[str] = ["Cliente", "Calibre", "KG Caja"]
    embarque_merger_contrato: lis[str] = [
        "RecieverName",
        "CaliberName",
        "PackageNetWeight",
    ]

    boleta_push: pd.DataFrame = embarques.merge(
        contratos, how="left", left_on=embarque_merger_contrato, right_on=contrato_key
    )
    boleta_push = boleta[["PalletRowId", "Cliente", "Precio"]]

    boleta = pd.concat([boleta, boleta_push], ignore_index=True)
    boleta.to_csv(boleta_path, index=False)

    return boleta
