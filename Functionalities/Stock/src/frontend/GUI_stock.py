"""
This module's purpose is to create the GUI for the stock management system.
"""

# Importing necessary libraries
import tkinter as tk
from tkinter import ttk
from tkinterdnd2 import *
import sys
from pathlib import Path

from typing import Union

# Import own modules
from src.frontend.GUI_tools.buttons import Boton
from src.frontend.GUI_tools.ventana import Ventana
from src.frontend.GUI_tools.info_window import InfoBoton
from src.config import universal_variables as univ
from src.frontend.GUI_tools import GUI_variables as var
from src.frontend.GUI_tools.file_select import BarraBusqueda

from ..backend.orchestrator import make_report
from src.config import universal_variables as univ


# Universal variables
bg = var.bg  # background color
fg = var.fg  # Text color
title = var.title  # Main window title
directory = univ.directory  # Base directory
stock_dir = univ.stock_dir  # Stock directory


def configure_download_button(download_button: Boton, barrasBusqueda: dict) -> None:
    """
    Function that configures the download button.
    Changes the command of the download button to the reporter function, which creates the stock report
    based on the selected files.

    Args:
        - download_button (Boton): Download button.
        - barrasBusqueda (dict): Dictionary containing the search bars.
    """

    def reporter():
        inputPaths = (
            {}
        )  # Diccionario que contiene los paths de los archivos seleccionados
        for tipo in barrasBusqueda:
            inputPaths[tipo] = Path(
                barrasBusqueda[tipo].get("1.0", "end-1c")
            ).as_posix()
        stock_path = Path(inputPaths["stock"])
        make_report(stock_path)

    download_button.configure(command=reporter)


def barras_maker(mainFrame: tk.Frame) -> tuple[dict, tk.Frame]:
    """
    Function that creates the search bars for the stock management window.

    Args:
        - mainFrame (tk.Frame): Main frame of the stock management window.

    Returns:
        - tuple[dict, tk.Frame]: Tuple containing the search bars and the frame.
    """

    frameBusqueda: tk.Frame = tk.Frame(mainFrame, bd=4, relief=tk.FLAT, bg=bg["window"])
    frameBusqueda.grid(row=0, column=0, sticky="ew")

    contents: dict = {
        "stock": "Selecciona un archivo .xls de stock",
    }

    barrasBusqueda: dict = {}
    for idx, tipo in enumerate(contents):
        barrasBusqueda[tipo] = BarraBusqueda(
            frameBusqueda,
            contents[tipo],
        )
        barrasBusqueda[tipo].grid(row=idx, column=0, sticky="ew")

    return barrasBusqueda, frameBusqueda


def final_buttons_maker(
    mainFrame: tk.Frame,
    padre: Union[tk.Tk, tk.Toplevel, TkinterDnD.Tk],
    root: Union[tk.Tk, tk.Toplevel, TkinterDnD.Tk],
) -> tuple[Boton, Boton, Boton, tk.Frame]:
    """
    Function that creates the final buttons for the stock management window.

    Args:
        - mainFrame (tk.Frame): Main frame of the stock management window.

    Returns:
        - tuple[Boton, tk.Frame]: Tuple containing the final buttons and the frame.
    """

    frameFinalButtons = tk.Frame(mainFrame, bd=4, bg=bg["window"])
    frameFinalButtons.grid(row=1, column=0, sticky="ew")

    def quitter():
        root.destroy()
        sys.exit()

    def go_back():
        root.destroy()
        padre.deiconify()

    salir = Boton(frameFinalButtons, "Salir", quitter, "exit_button")

    download_button = Boton(
        frameFinalButtons,
        "Download Stock Report",
        make_report,
        "output_button",
    )
    download_button.configure(width=250)

    def settings():
        if platform.system() == "Windows":
            os.startfile(ajustes_dir)
        elif platform.system() == "Darwin":  # macOS
            os.system(f'open "{ajustes_dir}"')  # HERE
        else:  # Linux and others
            os.system(f'xdg-open "{ajustes_dir}"')  # HERE

    ajustes = Boton(frameFinalButtons, "Ajustes", settings, "output_button")

    volver = Boton(
        frameFinalButtons,
        "Volver",
        go_back,
        "output_button",
    )

    if padre:
        volver.pack(side=tk.LEFT, anchor="n", padx=7, pady=(4, 0))
    ajustes.pack(side=tk.LEFT, anchor="n", padx=7, pady=(4, 0))
    # info.pack(side=tk.LEFT, anchor="n")
    salir.pack(side=tk.RIGHT, anchor="n")
    download_button.pack(side=tk.RIGHT, anchor="n")

    return download_button, salir, volver, frameFinalButtons


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
    root = stock_window.root
    mainFrame = stock_window.mainFrame

    barrasBusqueda, frameBusqueda = barras_maker(mainFrame)

    download_button, salir, volver, frameFinalButtons = final_buttons_maker(
        mainFrame, padre, root
    )

    configure_download_button(download_button, barrasBusqueda)

    return root


def stock_starter(padre: Union[tk.Tk, tk.Toplevel, TkinterDnD.Tk] = False) -> None:
    """
    Función que inicia la interfaz gráfica de la aplicación de pagos.
    Orquestra todos los elementos del modulo.
    """
    root = stock_window_maker(padre)

    if padre:
        root.protocol("WM_DELETE_WINDOW", padre.destroy)

    root.mainloop()

    return root
