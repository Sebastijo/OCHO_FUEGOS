"""
Automatisación de procesos corporativos: registro de gastos y ganacnias de la empresa.
El siguiente programa tiene como objetivo recibir archivos de Excel (a veces en formato PDF) y generar un reporte de gastos y ganancias de la empresa con detalles.
Empresa: Ocho Fuegos
Autor: Sebastián P. Pincheira
Fecha: 21/02/2024
Versión: 0.1.0
Lenguaje: Python 3.11.7
"""

__version__ = "0.1.0"

# importamos las librerias necesarias
import os
from typing import Union
import tkinter as tk
from tkinterdnd2 import *

from .src.config import variables as var

directory = var.directory


def run_controlador(padre: Union[tk.Tk, tk.Toplevel, TkinterDnD.Tk] = False) -> None:
    """
    Función que inicia la funcionalidad de controlador de la aplicación.
    La GUI se generará como un toplevel window de padre si es que se entrega.

    Args:
        padre (tk.Tk or TkinterDnD.Tk, optional): Ventana padre. Defaults to False.

    Returns:
        None

    Raises:
        None
    """
    # Obtenemos los paths que deben existir antes de correr el programa
    datos_folder = os.path.join(directory, "Datos del programa")
    variables_folder = os.path.join(datos_folder, "Variables")
    destination_cod_puerto_destino = os.path.join(
        variables_folder, "cod_puerto_destino.json"
    )
    destination_precios_contrato = os.path.join(
        variables_folder, "precios_contrato.xlsx"
    )
    destination_flete_real = os.path.join(variables_folder, "flete_real.xlsx")
    destination_costo_seco = os.path.join(variables_folder, "costo_seco.xlsx")
    output_folder = os.path.join(datos_folder, "output")

    config_paths = [
        variables_folder,
        destination_cod_puerto_destino,
        destination_precios_contrato,
        destination_flete_real,
        destination_costo_seco,
    ]

    if not all([os.path.exists(path) for path in config_paths]):
        # Creamos las carpeta de configuración en el dispositivo del usuario
        from .src.config.config_maker import make_config

        make_config()
        print("Información de Datos del programa>Variables actualizada.")

    # Creamos la carpeta de output en el dispositivo del usuario, de no existir.
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    # Iniciamos la interface de eusuario
    from .src.frontend.gui_ventas import controlador_starter

    root = controlador_starter(padre)

    return root
