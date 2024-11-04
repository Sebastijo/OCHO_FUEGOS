"""
This module's objective is to retrive the stock of the materials in the warehouse.
A 'packing' is the place were the 'materials' are stored.
"""

from pathlib import Path
import pandas as pd
import numpy as np

from .classes import Material, Packing


def read_data(
    stock_path: Path, kg2box_path: Path, box2material_path: Path
) -> list[Packing]:
    """
    Function that gets the stock of the materials in the warehouse.

    Args:
        - stock_path (Path): Path to the stock file.

    Returns: list[Packing]: List of the packings in the warehouse.

    Raises:
        - ValueError: If the stock file does not have the columns 'item' and 'stock'.
        - ValueError: If the stock limits file does not have the columns 'item', 'minimum_stock' and 'maximum_stock
    """

    def columns_checker(
        df: pd.DataFrame, needed_columns: set[str], df_name: str
    ) -> None:

        if not needed_columns <= set(df.columns):
            raise ValueError(
                f"{df_name} should have the columns {needed_columns} but has {set(df.columns)}."
            )

    paths = [stock_path, kg2box_path, box2material_path]

    for path in paths:
        if not path.exists():
            raise FileNotFoundError(f"File {path} not found.")
        if not path.is_file():
            raise FileNotFoundError(f"{path} is not a file.")
        if path.suffix != ".xlsx":
            raise FileNotFoundError(f"{path} should be an Excel file.")

    stock: dict[str, pd.DataFrame] = pd.read_excel(stock_path, sheet_name=None)
    kg = stock.pop("kg")
    kg2box: pd.DataFrame = pd.read_excel(kg2box_path)
    box2material: dict[str, pd.DataFrame] = pd.read_excel(
        box2material_path, sheet_name=None
    )

    stock_columns = {"CODIGO", "STOCK", "EMERGENCY STOCK", "DELIVERY TIME"}
    kg_columns = {"PACKING", "KG"}
    kg2box_columns = {"BOX TYPE", "BOXES PER 10KG"}
    box2material_columns = {"CODIGO", "X CAJA"}

    dfs: list[tuple[pd.DataFrame, set[str], str]] = (
        [(stock_df, stock_columns, "stock") for stock_df in stock.values()]
        + [(kg, kg_columns, "kg")]
        + [(kg2box, kg2box_columns, "kg2box")]
        + [
            (box2material_df, box2material_columns, "box2material")
            for box2material_df in box2material.values()
        ]
    )

    for df, columns, name in dfs:
        columns_checker(df, columns, name)

    return stock, kg, kg2box, box2material
