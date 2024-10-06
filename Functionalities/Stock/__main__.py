"""
Archvo __main__ para stock.
"""
# importamos las librerias necesarias
import os
from typing import Union
import tkinter as tk
from tkinterdnd2 import *

from src.config import universal_variables as univ

directory = univ.directory

def run_stock(padre: Union[tk.Tk, tk.Toplevel, TkinterDnD.Tk] = False) -> None:
    """
    Función que gatilla todo el programa de pagos.
    Esto prepara el inicio y lo inicia.

    Args:
        padre (tk.Tk or TkinterDnD.Tk, optional): Ventana padre. Defaults to False.
    
    Returns:
        None

    Raises:
        None
    """

    from .src.frontend.gui_stock import stock_starter

    root = stock_starter(padre)

    return root
