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


# A usefull class
class MoneyLabel:
    def __init__(
        self, frame: tk.Frame, cliente: str, bg: str, fg: str, initial_value: int = 0
    ):

        self.cliente = cliente

        # Create an IntVar for the money value
        self.money_var = tk.IntVar(value=initial_value)

        # Create a StringVar to hold the formatted display string
        self.money_label_var = tk.StringVar()

        # Trace changes to the IntVar
        self.money_var.trace("w", self.update_label)

        # Initialize the label text
        self.update_label()

        # Create the Label widget
        self.label = tk.Label(frame, textvariable=self.money_label_var, bg=bg, fg=fg)

    def update_label(self, *args):
        # Format the value with a dollar sign
        self.money_label_var.set(f"{self.cliente}: ${self.money_var.get()}")

    def set_value(self, value):
        # Update the money_var, which will trigger the label update
        self.money_var.set(value)

    def get_value(self):
        # Retrieve the current value
        return self.money_var.get()

    def add_value(self, value):
        # Add a value to the current value
        self.money_var.set(self.money_var.get() + value)

    def grid(self, **kwargs):
        self.label.grid(**kwargs)

    def pack(self, **kwargs):
        self.label.pack(**kwargs)

    def place(self, **kwargs):
        self.label.place(**kwargs)

    def destroy(self):
        self.label.destroy()


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
        "Cliente": (tk.OptionMenu, str, tk.StringVar()),
        "Fecha Pago": (DateEntry, str, tk.StringVar()),
        "País Destino": (tk.Entry, str, tk.StringVar()),
        "Ingreso": (tk.Entry, int, tk.IntVar()),
        "Observación": (tk.Entry, str, tk.StringVar()),
    }

    Clientes = ["Ejemplo1", "Ejemplo2", "Ejemplo3", "Ejemplo4"]

    Clientes_frame, Clientes_labels = client_display_maker(ventana, Clientes)

    features_frame, entries = feature_maker(ventana, features, Clientes_labels)

    buttom_buttons_frame, buttons = buttom_buttons(ventana, padre)

    return root, entries


def client_display_maker(
    ventana: Ventana, Clientes: list[str]
) -> tuple[tk.Frame, dict[tk.Label]]:
    """
    Función que crea el display de los clientes.

    Args:
        ventana (Ventana): Ventana principal de la GUI.
        Clientes (list[str]): Lista de clientes.

    Returns:
        tk.Frame: Frame donde se encuentran los elementos.
        dict: Diccionario con los elementos de la GUI.

    Raises:
        AssertionError: Si la ventana no es una instancia de Ventana.
        AssertionError: Si clientes no es una lista.
    """
    assert isinstance(
        ventana, Ventana
    ), f"ventana debe ser una instancia de Ventana. Se recibió {type(ventana)}"
    assert isinstance(
        Clientes, list
    ), f"clientes debe ser una lista. Se recibió {type(clientes)}"

    mainFrame = ventana.mainFrame

    Clientes_frame = tk.Frame(mainFrame, bd=4, relief=tk.SUNKEN, bg=bg["window"])
    Clientes_frame.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

    Clientes_labels = {cliente: None for cliente in Clientes}
    for i, cliente in enumerate(Clientes):
        Clientes_labels[cliente] = MoneyLabel(
            Clientes_frame, cliente=cliente, bg=bg["window"], fg=fg["window"]
        )
        Clientes_labels[cliente].grid(row=i, column=0, padx=5, pady=5, sticky="w")

    return Clientes_frame, Clientes_labels


def feature_maker(
    ventana: Ventana, features: dict, Clientes: dict[str, MoneyLabel]
) -> tuple[tk.Frame, dict[tuple[tk.Entry, tk.StringVar]]]:
    """
    Función que crea los elementos de la GUI.

    Args:
        ventana (Ventana): Ventana a la cual se le añadirán los elementos.
        features (dict): Diccionario con las características de los elementos.
        clientes (list[str]): Lista de clientes.

    Returns:
        tk.Frame: Frame donde se encuentran los elementos.
        dict: Diccionario con los elementos de la GUI.

    Raises:
        AssertionError: Si la ventana no es una instancia de Ventana.
        AssertionError: Si features no es un diccionario.
        AssertionError: Si clientes no es una lista.
    """
    assert isinstance(
        ventana, Ventana
    ), f"ventana debe ser una instancia de Ventana. Se recibió {type(ventana)}"
    assert isinstance(
        features, dict
    ), f"features debe ser un diccionario. Se recibió {type(features)}"
    assert isinstance(
        Clientes, dict
    ), f"clientes debe ser una dicccionario. Se recibió {type(clientes)}"

    mainFrame = ventana.mainFrame

    features_frame = tk.Frame(mainFrame, bd=4, relief=tk.SUNKEN, bg=bg["window"])
    features_frame.grid(row=0, column=0, padx=5, pady=5)

    elements_per_column = len(features) // 2

    entries = {feature: None for feature in features}

    for i, (feature, kind) in enumerate(features.items()):
        widget = kind[0]
        data_type = kind[1]
        Var = kind[2]
        row = i % elements_per_column
        column = i // elements_per_column
        feature_label = tk.Label(
            features_frame, text=feature, bg=bg["window"], fg=fg["window"]
        )
        feature_label.grid(row=row, column=column * 2, padx=5, pady=5)
        if widget == tk.OptionMenu:
            feature_entry = widget(features_frame, Var, *Clientes)
            feature_entry.config(width=16)
        else:
            feature_entry = widget(features_frame, textvariable=Var, width=20)
            feature_entry.insert(0, data_type())
        feature_entry.grid(row=row, column=column * 2 + 1, padx=5, pady=5)
        entries[feature] = (feature_entry, Var)

    def ingresar():
        """
        Función que ingresa los datos de la GUI a la base de datos.
        """
        cliente = features["Cliente"][2].get()
        ingreso = features["Ingreso"][2].get()
        Clientes[cliente].add_value(ingreso)

    last_element_idx = len(features)
    row = last_element_idx % elements_per_column
    column = last_element_idx // elements_per_column
    ingresar_button = Boton(
        features_frame,
        "Ingresar",
        ingresar,
        "output_button",
    )
    ingresar_button.grid(
        row=row, column=column * 2, padx=5, pady=5, columnspan=2, sticky="e"
    )

    return features_frame, entries


def buttom_buttons(
    ventana: Ventana, padre: Union[tk.Tk, tk.Toplevel, TkinterDnD.Tk]
) -> tuple[tk.Frame, dict[Boton]]:
    """
    El objetivo de esta función es crear los botones finales de la GUI.

    Args:
        ventana (Ventana): Ventana principal de la GUI.
        padre (Union[tk.Tk, tk.Toplevel, TkinterDnD.Tk]): Ventana padre de la GUI.

    Returns:
        tk.Frame: Frame donde se encuentran los botones.
        dict[Boton]: Diccionario con los botones de la GUI.

    Raises:
        AssertionError: Si la ventana no es una instancia de Ventana.
        AssertionError: Si el padre no es una instancia de tk.Tk, tk.Toplevel o TkinterDnD.Tk.
    """
    assert isinstance(
        ventana, Ventana
    ), f"ventana debe ser una instancia de Ventana. Se recibió {type(ventana)}"
    assert isinstance(
        padre, (tk.Tk, tk.Toplevel, TkinterDnD.Tk)
    ), f"padre debe ser una instancia de tk.Tk, tk.Toplevel o TkinterDnD.Tk. Se recibió {type(padre)}"

    root = ventana.root
    mainFrame = ventana.mainFrame

    buttom_buttons_frame = tk.Frame(mainFrame, bd=4, relief=tk.FLAT, bg=bg["window"])
    buttom_buttons_frame.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

    def quitter():
        root.destroy()
        sys.exit()

    def go_back():
        root.destroy()
        padre.deiconify()

    buttons = {
        "Volver": Boton(
            buttom_buttons_frame,
            "Volver",
            go_back,
            "output_button",
        ),
        "Salir": Boton(buttom_buttons_frame, "Salir", quitter, "exit_button"),
    }

    buttons["Volver"].pack(side=tk.LEFT, padx=5, pady=5)
    buttons["Salir"].pack(side=tk.RIGHT, padx=5, pady=5)

    return buttom_buttons_frame, buttons


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
