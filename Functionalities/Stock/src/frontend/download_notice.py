"""
The objective of this module is to vreate a simple pop up message notifying the user that the download completed successfully.
"""

# Importing necessary libraries
import tkinter as tk
from tkinter import ttk
from tkinterdnd2 import *
import sys
from pathlib import Path
from typing import Union
from datetime import date


# Import own modules
from src.frontend.GUI_tools.buttons import Boton
from src.frontend.GUI_tools.ventana import Ventana
from src.frontend.GUI_tools import GUI_variables as var

# Universal variables
bg = var.bg  # background color
fg = var.fg  # Text color
title = var.title  # Main window title


def download_notice(
    padre: Union[tk.Tk, tk.Toplevel, TkinterDnD.Tk], pdf_path: Path
) -> None:
    """
    Function that creates a simple pop up message notifying the user that the download completed successfully.
    """

    ventana = Ventana(titulo="Descarga completada", padre=padre)

    root = ventana.root
    mainFrame = ventana.mainFrame

    text = (
        "Descarga del reporte de stock completada con éxito.\n"
        "Se encuentra disponible en.\n"
        f"{pdf_path}"
    )

    # Creating a single Label with the multiline text
    label = ttk.Label(
        mainFrame, text=text, background=bg["window_text"], foreground=fg["window_text"]
    )

    label.grid(row=0, column=0, padx=10, pady=10)

    # Button
    button = Boton(mainFrame, "OK", root.destroy, "output_button")

    button.grid(row=3, column=0, padx=10, pady=10)
