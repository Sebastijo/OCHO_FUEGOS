"""
El objetivo de este modulo es crear una boleta a partir de la base control y los contratos con los clientes,
la cual es guardada en un archivo .csv junto al control de pagos. Esta posteriormente será usada para descontar.
"""

import pandas as pd
from pathlib import Path
from typing import Union

from src.config.universal_variables import (
    pagos_dir,
    embarque_path_pointer,
    contratos_path_pointer,
    get_pointer_path,
)

boleta_path = pagos_dir / "boleta.csv"

embarques_path = get_pointer_path(embarque_path_pointer, "base de embarques")
contratos_path = get_pointer_path(contratos_path_pointer, "base de contratos")


def actualizar_boleta() -> Union[pd.DataFrame, Exception]:
    """
    Crea una boleta a partir de la base control y los contratos con los clientes.
    Revisa el formato de embarques y contratos para asegurarse de que sean correctos.

    Args: None

    Returns:
        - pd.DataFrame: DataFrame con la boleta actualizada.
        - Exception: Excepción que se produjo al intentar cargar los archivos.
    """
    try:
        boleta: pd.DataFrame = pd.read_csv(boleta_path)
    except FileNotFoundError:
        boleta_dict: dict[str, any] = {
            "PalletRowId": [],
            "Cliente": [],
            "Precio": [],
        }
        boleta: pd.DataFrame = pd.DataFrame(boleta_dict)

    # Importamos la base embarque quedandonos solo con los elementos que no están en la boleta
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
        if not {
            "PalletRowId",
            "ReceiverName",
            "CaliberName",
            "PackageNetWeight",
            "Quantity",
        } <= set(embarques.columns):
            raise Exception(
                "La base de embarques no tiene las columnas necesarias: PalletRowId, ReceiverName, CaliberName, PackageNetWeight, Quantity."
            )
        # we check all elements are numeric for PackageNetWeight and Quantity
        if (
            not embarques["PackageNetWeight"]
            .apply(lambda x: isinstance(x, (int, float)))
            .all()
        ):
            raise Exception(
                "La columna PackageNetWeight de la base de embarques no es numérica."
            )
        if not embarques["Quantity"].apply(lambda x: isinstance(x, (int, float))).all():
            raise Exception(
                "La columna Quantity de la base de embarques no es numérica."
            )
    except Exception as e:
        e = Exception(
            "No se pudo cargar el archivo ubicado en: "
            + str(embarques_path)
            + ". "
            + "El error es el siguiente:\n"
            + str(e)
        )
        return e

    embarques = embarques.merge(
        boleta[["PalletRowId"]], how="left", on="PalletRowId", indicator=True
    )
    embarques = embarques[embarques["_merge"] == "left_only"].drop("_merge", axis=1)

    try:
        contratos: pd.DataFrame = pd.read_excel(contratos_path)
        if not {"Cliente", "Calibre", "KG Caja", "Precio"} <= set(contratos.columns):
            raise Exception(
                "La base de contratos no tiene las columnas necesarias: Cliente, Calibre, KG Caja, Precio."
            )
        # we check all elements are numeric for KG Caja and Precio
        if not contratos["KG Caja"].apply(lambda x: isinstance(x, (int, float))).all():
            raise Exception(
                "La columna KG Caja de la base de contratos no es numérica."
            )
        if not contratos["Precio"].apply(lambda x: isinstance(x, (int, float))).all():
            raise Exception("La columna Precio de la base de contratos no es numérica.")
    except Exception as e:
        e = Exception(
            "No se pudo cargar el archivo ubicado en: "
            + str(contratos_path)
            + "."
            + "El error es el siguiente:\n"
            + str(e)
        )
        return e

    # A cada elemento de embarques le asignamos un precio

    contrato_key: list[str] = ["Cliente", "Calibre", "KG Caja"]
    embarque_merger_contrato: lis[str] = [
        "ReceiverName",
        "CaliberName",
        "PackageNetWeight",
    ]

    boleta_push: pd.DataFrame = embarques.merge(
        contratos, how="left", left_on=embarque_merger_contrato, right_on=contrato_key
    )

    boleta_push["Precio"] = boleta_push["Precio"] * boleta_push["Quantity"]

    boleta_push = boleta_push[["PalletRowId", "Cliente", "Precio"]]

    boleta = pd.concat([boleta, boleta_push], ignore_index=True)
    boleta.to_csv(boleta_path, index=False)

    return boleta
