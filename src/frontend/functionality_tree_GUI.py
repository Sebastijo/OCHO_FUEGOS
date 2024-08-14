"""
Ventana con las distintas funcionalidades de la aplicación.
"""

# Importación de bibliotecas necesarias
import tkinter as tk
from tkinter import ttk
from tkinterdnd2 import *
import pandas as pd
from pathlib import Path
import os
import threading
import traceback

# Importamos paquetes propios

if __name__ == "__main__":
    from src.frontend.GUI_tools.ventana import Ventana
    from src.frontend.GUI_tools.buttons import Boton
    from src.config import universal_variables as univ
    from src.frontend.GUI_tools import GUI_variables as var
    from Functionalities.Controlador.src.frontend.gui_ventas import controlador_starter
    pagos_starter = lambda: print("Funcionalidad no implementada")
else:
    from .GUI_tools.ventana import Ventana
    from .GUI_tools.buttons import Boton
    from ..config import universal_variables as univ
    from .GUI_tools import GUI_variables as var
    from ...Functionalities.Controlador.src.frontend.gui_ventas import controlador_starter
    pagos_starter = lambda: print("Funcionalidad no implementada")

# Variables universales:
bg = var.bg  # Color de fondo
fg = var.fg  # Color de texto
title = var.title  # Título de la ventana principal
directory = univ.directory  # Directorio de trabajo

def functionality_tree_window_maker():

    """
    Función que crea la ventana principal con las distintas funcionalidades de la aplicación.

    Args:
        None
    
    Returns:
        None
    
    Raises:
        None
    """

    # Creación de la ventana principal utilizando tkinter
    ventana = Ventana(titulo=title["main"])
    root = ventana.root
    mainFrame = ventana.mainFrame

    functionalities = {"Base Control": controlador_starter, "Pagos": pagos_starter}
    buttons = {}

    for idx, functionality in enumerate(functionalities):
        buttons[functionality] = Boton(
            mainFrame,
            text=functionality,
            command=lambda: print("Funcionalidad no implementada"),
            style="output_button",
            width=175,
        )

        (
            buttons[functionality].pack(padx=100, pady=(35, 5))
            if idx == 0
            else buttons[functionality].pack(padx=100, pady=5)
        )

    exit_button = Boton(mainFrame, text="Salir", command=root.quit, style="exit_button", width=100,)
    exit_button.pack(padx=100, pady=(20,25))

    for functionality in functionalities:
        buttons[functionality].config(command=functionalities[functionality])

    root.mainloop()

if __name__ == "__main__":
    functionality_tree_window_maker()