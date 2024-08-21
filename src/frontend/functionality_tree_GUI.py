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
import sys
import threading

# Importamos paquetes propios

if __name__ == "__main__":
    from src.frontend.GUI_tools.ventana import Ventana
    from src.frontend.GUI_tools.buttons import Boton
    from src.config import universal_variables as univ
    from src.frontend.GUI_tools import GUI_variables as var
    from Functionalities.Controlador.__main__ import run_controlador
    from Functionalities.Pagos.__main__ import run_pagos
else:
    from .GUI_tools.ventana import Ventana
    from .GUI_tools.buttons import Boton
    from ..config import universal_variables as univ
    from .GUI_tools import GUI_variables as var
    from Functionalities.Controlador.__main__ import run_controlador
    from Functionalities.Pagos.__main__ import run_pagos

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
    ventana = Ventana(titulo=title["main"], DnD=True)
    root = ventana.root
    mainFrame = ventana.mainFrame

    def execute_and_destroy_window(function: callable) -> callable:
        """
        Función que recibe una función y entrega una función que realiza lo mismo y que, además, oculta la ventana principal.
        La función recibida debe crear una ventana y devolver esta ventana como output.
        Como input, debe recibir una ventana padre.

        Args:
            function (callable): Función a ejecutar. Debe recibir como argumento la ventana principal.

        Returns:
            callable: Función que ejecuta la función entregada y oculta la ventana principal.

        Raises:
            AssertionError: Si la función entregada no es callable.
        """
        assert callable(function), "La función entregada no es callable."

        def wrapper():
            ventana.root.withdraw()
            try:
                child = function(ventana.root)
            except Exception as e:
                print(f"Error: {e}")
                traceback.print_exc()

        return wrapper

    functionalities = {
        "Base Control": execute_and_destroy_window(run_controlador),
        "Pagos": execute_and_destroy_window(run_pagos),
    }
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

    def quitter():
        root.destroy()
        sys.exit()

    exit_button = Boton(
        mainFrame,
        text="Salir",
        command=quitter,
        style="exit_button",
        width=100,
    )
    exit_button.pack(padx=100, pady=(20, 25))

    for functionality in functionalities:
        buttons[functionality].configure(command=functionalities[functionality])

    root.mainloop()


if __name__ == "__main__":
    functionality_tree_window_maker()
