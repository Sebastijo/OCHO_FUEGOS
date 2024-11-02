"""
This module's objective is to orchestrate the stock functionalities.
"""

from pathlib import Path
import pandas as pd
import os
from datetime import date

from .data_loader import Material, Packing, get_stock
from .pdf_maker import create_stock_report

today = date.today().strftime("%d_%m_%Y")

home = Path.home()
downloads = home / "Downloads"
file_name = "stock_report_" + today + ".pdf"
pdf_path = downloads / file_name


def make_report(stock_path: Path, stock_limits_path: Path) -> None:
    """
    Function that creates a stock report.

    Args:
        - stock_path (Path): Path to the stock file.

    Returns: None
    """

    packings: list[Packing] = get_stock(stock_path, stock_limits_path)
    create_stock_report(pdf_path, packings)
