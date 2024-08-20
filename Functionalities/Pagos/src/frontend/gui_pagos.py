"""
El objetivo de este mdoulo es crear la interfaz gráfica de la aplicación de pagos.
"""

# Importación de bibliotecas necesarias
import tkinter as tk
from tkinter import ttk
from tkinterdnd2 import *
from tkcalendar import DateEntry
import pandas as pd
from pathlib import Path
import os
import threading
import traceback
from typing import Union
import sys

# Importamos modulos propios
from src.frontend.GUI_tools.buttons import Boton
from src.frontend.GUI_tools.ventana import Ventana

# from src.frontend.GUI_tools.info_window import InfoBoton
from src.frontend.GUI_tools.error_window import inputErrorWindow, revisarWindow
from src.config import universal_variables as univ
from src.frontend.GUI_tools import GUI_variables as var

# Variables universales:
bg = var.bg  # Color de fondo
fg = var.fg  # Color de texto
title = var.title  # Título de la ventana principal
directory = univ.directory  # Directorio de trabajo


def main_window_maker(
    padre: Union[tk.Tk, tk.Toplevel, TkinterDnD.Tk] = False
) -> tuple[tk.Tk, dict, tk.Frame, list, tk.Tk, Boton, ttk.Progressbar]:
    """
    Función que define los objetos y posiciones de la GUI.

    Args:
        padre (tk.Tk or TkinterDnD.Tk, optional): Ventana padre. Defaults to False.

    Returns:
        root: Ventana principal de la GUI.
        entries: Diccionario con los entries de la GUI.

    Raises:
        AssertionError: Si el padre no es una instancia de tk.Tk o TkinterDnD.Tk, tk.Toplevel o False.
    """
    assert isinstance(padre, (tk.Tk, tk.Toplevel, TkinterDnD.Tk)) or padre == False

    # Creación de la ventana principal utilizando tkinter
    ventana = Ventana(titulo=title["main"], DnD=True, padre=padre)
    root = ventana.root
    mainFrame = ventana.mainFrame

    features = {
        "Cliente": (tk.OptionMenu, str),
        "Fecha Pago": (DateEntry, str),
        "País Destino": (tk.Entry, str),
        "Ingreso": (tk.Entry, int),
        "Observación": (tk.Entry, str),
    }

    Nombres = ["Ejemplo1", "Ejemplo2", "Ejemplo3", "Ejemplo4"]
    Nombre_Var = tk.StringVar()
    Nombre_Var.set("Nombre")

    features_frame = tk.Frame(mainFrame, bd=4, relief=tk.FLAT, bg=bg["window"])
    features_frame.grid(row=0, column=0, padx=5, pady=5)

    elements_per_column = len(features) // 2

    entries = {feature: None for feature in features}

    for i, (feature, kind) in enumerate(features.items()):
        widget = kind[0]
        data_type = kind[1]
        row = i % elements_per_column
        column = i // elements_per_column
        feature_label = tk.Label(
            features_frame, text=feature, bg=bg["window"], fg=fg["window"]
        )
        feature_label.grid(row=row, column=column * 2, padx=5, pady=5)
        if widget == tk.OptionMenu:
            feature_entry = widget(features_frame, Nombre_Var, *Nombres)
            feature_entry.config(width=16)
        else:
            feature_entry = widget(
                features_frame, width=20
            )  # bg=bg["entry"], fg=fg["entry"]
            feature_entry.insert(0, data_type())
        feature_entry.grid(row=row, column=column * 2 + 1, padx=5, pady=5)
        entries[feature] = feature_entry
    return root, entries


def pagos_starter(padre: Union[tk.Tk, tk.Toplevel, TkinterDnD.Tk] = False) -> None:
    """
    Función que inicia la interfaz gráfica de la aplicación de pagos.
    Orquestra todos los elementos del modulo.
    """
    root, entries = main_window_maker(padre)

    if padre:
        root.protocol("WM_DELETE_WINDOW", padre.destroy)
        
    root.mainloop()

    return root
