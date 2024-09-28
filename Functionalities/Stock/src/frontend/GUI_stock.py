"""
This module's purpose is to create the GUI for the stock management system.
"""

# Importing necessary libraries
import tkinter as tk
from tkinter import ttk
from tkinterdnd2 import *

from typing import Union

# Import own modules
from src.frontend.GUI_tools.buttons import Boton
from src.frontend.GUI_tools.ventana import Ventana
from src.frontend.GUI_tools.info_window import InfoBoton
from src.config import universal_variables as univ
from src.frontend.GUI_tools import GUI_variables as var

# Universal variables
bg = var.bg  # background color
fg = var.fg  # Text color
title = var.title  # Main window title
directory = univ.directory  # Base directory


def stock_window_maker(
    padre: Union[tk.Tk, tk.Toplevel, TkinterDnD.Tk] = False
) -> tuple:
    """
    Function that defines the widgets and positions of the stock management window.

    Args: padre (tk.Tk, tk.Toplevel, TkinterDnD.Tk): Parent window of the stock management window.  Defaults to False.

    Returns: tuple: Tuple containing the main window and the frame.

    Raises:
        TypeError: If the padre argument is not a Tkinter window or a bool.
    """

    # Check if the padre argument is a Tkinter window or a bool
    if not isinstance(padre, (tk.Tk, tk.Toplevel, TkinterDnD.Tk, bool)):
        raise TypeError(
            f"The padre argument must be a Tkinter window or a bool, not {type(padre)}."
        )

    # Create the main window
    stock_window = Ventana(titulo=title["main"], DnD=True, padre=padre)
    root = stock_window.ventana
    mainFrame = stock_window.mainFrame

    return
