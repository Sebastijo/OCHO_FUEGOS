"""
This module's objective is to orchestrate the stock functionalities.
"""

from pathlib import Path
import pandas as pd
import os
from datetime import date

from .data_loader import read_data
from .pdf_maker import create_stock_report
from .classes import Packing
from .history import append_packing_history

# today = date.today().strftime("%d_%m_%Y")

# home = Path.home()
# downloads = home / "Downloads"
# file_name = "stock_report_" + today + ".pdf"
# pdf_path = downloads / file_name


def make_report(stock_path: Path, kg2box_path: Path, box2material_path: Path) -> Path:
    """
    Function that creates a stock report.

    Args:
        - stock_path (Path): Path to the stock file.
        - kg2box_path (Path): Path to the kg2box file.
        - box2material_path (Path): Path to the box2material file.

    Returns:
        - pdf_path (Path): Path to the created PDF file.

    Raises:
        - FileNotFoundError: If any of the files is not found.
        - ValueError: If any of the files is not an Excel file.
        - ValueError: If the stock file does not have the columns 'item' and 'stock'.
        - ValueError: If the stock limits file does not have the columns 'item', 'minimum_stock' and 'maximum
    """

    packings_dict, kg, kg2box_df, box2material_dict = read_data(
        stock_path, kg2box_path, box2material_path
    )

    packings: list[Packing] = [
        Packing(name, materials, kg2box_df, box2material_dict)
        for name, materials in packings_dict.items()
    ]

    for packing in packings:
        kg_float: float = kg.loc[kg["PACKING"] == packing.name, "KG"].values[0]
        packing.update_minimum_and_maximum_stocks(kg_float)

    file_path = append_packing_history(packings)
    # create_stock_report(pdf_path, packings)

    return file_path
