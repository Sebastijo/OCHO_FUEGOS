"""
This module's objective is to retrive the stock of the materials in the warehouse.
A 'packing' is the place were the 'materials' are stored.
"""

from pathlib import Path
import pandas as pd
import numpy as np

from .classes import Material, Packing


def stock_file_format_checker(stock_path: Path, stock_limits_path: Path) -> None:
    """
    Function that checks if the stock files are in the correct format.

    Args:
        - stock_path (Path): Path to the stock file.
        - stock_limits_path (Path): Path to the stock limits file.

    Returns: None

    Raises:
        - FileNotFoundError: If the stock file is not found.
        - FileNotFoundError: If the stock limits file is not found.
        - FileNotFoundError: If the stock file is not a file.
        - FileNotFoundError: If the stock limits file is not a file.
        - FileNotFoundError: If the stock file is not an Excel file.
        - FileNotFoundError: If the stock limits file is not an Excel file.
    """
    for path in [stock_path, stock_limits_path]:
        if not path.exists():
            raise FileNotFoundError(f"File {path} not found.")
        if not path.is_file():
            raise FileNotFoundError(f"{path} is not a file.")
        if path.suffix != ".xlsx":
            raise FileNotFoundError(f"{path} should be an Excel file.")


def get_stock(stock_path: Path, stock_limits_path: Path) -> list[Packing]:
    """
    Function that gets the stock of the materials in the warehouse.

    Args:
        - stock_path (Path): Path to the stock file.

    Returns: list[Packing]: List of the packings in the warehouse.

    Raises:
        - ValueError: If the stock file does not have the columns 'item' and 'stock'.
        - ValueError: If the stock limits file does not have the columns 'item', 'minimum_stock' and 'maximum_stock
    """

    stock_file_format_checker(stock_path, stock_limits_path)

    stock: list[pd.DataFrame] = [
        pd.read_excel(stock_path, sheet_name="packing_0").sort_values(by="item"),
        pd.read_excel(stock_path, sheet_name="packing_1").sort_values(by="item"),
    ]
    stock_limits: list[pd.DataFrame] = [
        pd.read_excel(stock_limits_path, sheet_name="packing_0").sort_values(by="item"),
        pd.read_excel(stock_limits_path, sheet_name="packing_1").sort_values(by="item"),
    ]

    for stock_df in stock:
        if not {"item", "stock"} <= set(stock_df.columns):
            raise ValueError(
                "The stock file should have the columns 'item' and 'stock'."
            )

    for stock_limits_df in stock_limits:
        if not {"item", "minimum_stock", "maximum_stock"} <= set(
            stock_limits_df.columns
        ):
            raise ValueError(
                "The stock limits file should have the columns 'item', 'minimum_stock' and 'maximum_stock'."
            )

    if len(stock[0]) != len(stock_limits[0]) or len(stock[1]) != len(stock_limits[1]):
        raise ValueError(
            "The stock and stock limits files should have the same length."
        )

    if (
        stock[0]["item"].to_list() != stock_limits[0]["item"].to_list()
        or stock[1]["item"].to_list() != stock_limits[1]["item"].to_list()
    ):
        raise ValueError(
            "The items in the stock and stock limits files should be the same."
        )

    materials: list[np.array[Material]] = [
        np.empty(len(stock[0]), dtype=Material),
        np.empty(len(stock[1]), dtype=Material),
    ]

    for idx, packing in enumerate(materials):
        for i in range(len(packing)):
            assert (
                stock[idx]["item"][i] == stock_limits[idx]["item"][i]
            ), "The items in the stock and stock limits files should be the same."
            material = Material(stock[idx]["item"][i], stock[idx]["stock"][i])
            material.set_limits(
                stock_limits[idx]["minimum_stock"][i],
                stock_limits[idx]["maximum_stock"][i],
            )
            packing[i] = material

    packings = [Packing("packing_0", materials[0]), Packing("packing_1", materials[1])]

    return packings
