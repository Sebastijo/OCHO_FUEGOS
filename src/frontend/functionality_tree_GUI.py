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
    from Functionalities.Controlador.__main__ import run_controlador

    run_pagos = lambda: print("Funcionalidad no implementada")
else:
    from .GUI_tools.ventana import Ventana
    from .GUI_tools.buttons import Boton
    from ..config import universal_variables as univ
    from .GUI_tools import GUI_variables as var
    from Functionalities.Controlador.__main__ import run_controlador

    run_pagos = lambda: print("Funcionalidad no implementada")

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

    def execute_and_destroy_window(function: callable) -> callable:
        """
        Funcional que recibe una función y entrega una función que leariza lo mismo y que, además, destruye la ventana principal.

        Args:
            function (callable): Función a ejecutar.

        Returns:
            callable: Función que ejecuta la función entregada y destruye la ventana principal.

        Raises:
            None
        """

        def wrapper():
            ventana.root.destroy()
            function(False)

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

    exit_button = Boton(
        mainFrame,
        text="Salir",
        command=root.quit,
        style="exit_button",
        width=100,
    )
    exit_button.pack(padx=100, pady=(20, 25))

    for functionality in functionalities:
        buttons[functionality].configure(command=functionalities[functionality])

    root.mainloop()


if __name__ == "__main__":
    functionality_tree_window_maker()
