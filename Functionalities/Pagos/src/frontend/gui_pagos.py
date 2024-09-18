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
import platform

# Importamos modulos propios
from src.frontend.GUI_tools.buttons import Boton
from src.frontend.GUI_tools.ventana import Ventana
from ..backend.control_de_pagos import agregar_pago
from ..backend.calcular_money_label import actualizar_moneyLabels
from src.frontend.GUI_tools.info_window import InfoBoton
from src.frontend.GUI_tools.error_window import inputErrorWindow, revisarWindow
from src.config import universal_variables as univ
from src.frontend.GUI_tools import GUI_variables as var
from .moneyLabel import MoneyLabel
from ..backend.clientes import update_clients
from ..backend.boleta import actualizar_boleta

# Variables universales:
bg = var.bg  # Color de fondo
fg = var.fg  # Color de texto
title = var.title  # Título de la ventana principal
directory = univ.directory  # Directorio de trabajo
pagos_dir = univ.pagos_dir  # Directorio de pagos


def main_window_maker(
    padre: Union[tk.Tk, tk.Toplevel, TkinterDnD.Tk] = False
) -> tuple[tk.Tk, dict[tuple[tk.Entry, tk.StringVar]]]:
    """
    Función que define los objetos y posiciones de la GUI.

    Args:
        padre (tk.Tk or TkinterDnD.Tk, optional): Ventana padre. Defaults to False.

    Returns:
        root: Ventana principal de la GUI.
        entries: Diccionario con los entries de la GUI.
        Clientes_labels: Diccionario con los MoneyLabels de los clientes.

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

    Clientes = update_clients()

    Clientes_frame, Clientes_labels = client_display_maker(ventana, Clientes)

    features_frame, entries, ingresar_button = feature_maker(
        ventana, features, Clientes_labels
    )

    buttom_buttons_frame, buttons = buttom_buttons(ventana, padre, ingresar_button)

    return root, entries


def client_display_maker(
    ventana: Ventana, Clientes: list[str]
) -> tuple[tk.Frame, dict[str, MoneyLabel]]:
    """
    Función que crea el display de los clientes.
    Para crear el display, se calcula el saldo de cada cliente mediante la función `actualizar_moneyLabels`.

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
    ), f"clientes debe ser una lista. Se recibió {type(Clientes)}"

    mainFrame = ventana.mainFrame

    Clientes_frame = tk.Frame(mainFrame, bd=4, relief=tk.SUNKEN, bg=bg["window"])
    Clientes_frame.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

    Clientes_labels: dict[str, MoneyLabel] = {cliente: None for cliente in Clientes}
    for i, cliente in enumerate(Clientes):
        Clientes_labels[cliente] = MoneyLabel(
            Clientes_frame, cliente=cliente, bg=bg["window"], fg=fg["window"]
        )
        Clientes_labels[cliente].grid(row=i, column=0, padx=5, pady=5, sticky="w")

    actualizar_boleta()

    actualizar_moneyLabels(Clientes_labels.values())

    return Clientes_frame, Clientes_labels


def feature_maker(
    ventana: Ventana, features: dict, Clientes: dict[str, MoneyLabel]
) -> tuple[tk.Frame, dict[tuple[tk.Entry, tk.StringVar]], Boton]:
    """
    Función que crea los elementos de la GUI.

    Args:
        ventana (Ventana): Ventana a la cual se le añadirán los elementos.
        features (dict): Diccionario con las características de los elementos.
        clientes (list[str]): Lista de clientes.

    Returns:
        tk.Frame: Frame donde se encuentran los elementos.
        dict: Diccionario con los elementos de la GUI.
        ingresar_button: Botón de ingresar (datos).

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

        # nos aseguramos de que el ingreso sea un número
        if feature == "Ingreso":

            def validate_numeric_input(action, value_if_allowed):
                if action != "1":  # If the action is not insertion (deletion is fine)
                    return True
                try:
                    # Check if the input is a valid float number
                    float(value_if_allowed)
                    return True
                except ValueError:
                    return False

            validate_numeric_input_command = (
                features_frame.register(validate_numeric_input),
                "%d",
                "%P",
            )
            feature_entry.config(
                validate="key", validatecommand=validate_numeric_input_command
            )

        entries[feature] = (feature_entry, Var)

    def ingresar():
        """
        Función que ingresa los datos de la GUI a la base de datos.
        """
        # Actualizamos la boleta con los nuevos datos de embarque
        actualizar_boleta()

        # Obtener los valores a ingresar
        cliente = features["Cliente"][2].get()
        cliente = Clientes[cliente]
        ingreso = features["Ingreso"][2].get()
        ingreso = float(ingreso)
        pais = features["País Destino"][2].get()
        fecha = features["Fecha Pago"][2].get()
        observacion = features["Observación"][2].get()

        # Agregamos el pago al control de pagos
        agregar_pago(cliente, fecha, pais, ingreso, observacion)

        # ACtualizamos los valores de los MoneyLabels
        actualizar_moneyLabels([cliente])

    last_element_idx = len(features)
    row = last_element_idx % elements_per_column
    column = last_element_idx // elements_per_column
    ingresar_button = Boton(
        features_frame,
        "Ingresar",
        ingresar,
        "output_button",
    )
    ingresar_button.command = ingresar  # This WILL be modified in buttom_buttons
    ingresar_button.grid(
        row=row, column=column * 2, padx=5, pady=5, columnspan=2, sticky="e"
    )

    return features_frame, entries, ingresar_button


def buttom_buttons(
    ventana: Ventana,
    padre: Union[tk.Tk, tk.Toplevel, TkinterDnD.Tk],
    ingresar_button: Boton,
) -> tuple[tk.Frame, dict[Boton]]:
    """
    El objetivo de esta función es crear los botones finales de la GUI.

    Args:
        ventana (Ventana): Ventana principal de la GUI.
        padre (Union[tk.Tk, tk.Toplevel, TkinterDnD.Tk]): Ventana padre de la GUI.
        ingresar_button (Boton): Botón de ingresar.

    Returns:
        tk.Frame: Frame donde se encuentran los botones.
        dict[Boton]: Diccionario con los botones de la GUI.

    Raises:
        AssertionError: Si la ventana no es una instancia de Ventana.
        AssertionError: Si el padre no es una instancia de tk.Tk, tk.Toplevel o TkinterDnD.Tk.
        AsserionError: Si ingresar_button no es una instancia de Boton.
    """
    assert isinstance(
        ventana, Ventana
    ), f"ventana debe ser una instancia de Ventana. Se recibió {type(ventana)}"
    assert isinstance(
        padre, (tk.Tk, tk.Toplevel, TkinterDnD.Tk)
    ), f"padre debe ser una instancia de tk.Tk, tk.Toplevel o TkinterDnD.Tk. Se recibió {type(padre)}"
    assert isinstance(
        ingresar_button, Boton
    ), f"ingresar_button debe ser una instancia de Boton. Se recibió {type(ingresar_button)}"

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

    def settings():
        if platform.system() == "Windows":
            os.startfile(pagos_dir)
        elif platform.system() == "Darwin":  # macOS
            os.system(f"open {pagos_dir}")
        else:  # Linux and others
            os.system(f"xdg-open {pagos_dir}")

    buttons = {
        "Volver": Boton(
            buttom_buttons_frame,
            "Volver",
            go_back,
            "output_button",
        ),
        "Ajustes": Boton(buttom_buttons_frame, "Ajustes", settings, "output_button"),
        "Salir": Boton(buttom_buttons_frame, "Salir", quitter, "exit_button"),
    }

    buttons["Volver"].pack(side=tk.LEFT, padx=5, pady=5)
    buttons["Ajustes"].pack(side=tk.LEFT, padx=5, pady=5)
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
