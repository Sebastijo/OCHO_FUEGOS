"""
ElThis module's objective is to orchestrate the stock functionalities.
"""

from pathlib import Path
import pandas as pd

from .data_loader import Material, Packing, get_stock
from .pdf_maker import create_stock_report

pdf_path = Path(__file__).resolve().parents[2] / "data" / "stock_report.pdf"


def make_report(stock_path: Path) -> None:
    """
    Function that creates a stock report.

    Args:
        - stock_path (Path): Path to the stock file.

    Returns: None
    """

    packings: list[Packing] = get_stock(stock_path)
    create_stock_report(pdf_path, packings)
