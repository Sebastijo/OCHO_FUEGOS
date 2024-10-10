"""
El objetivo de este modulo es crear el archivo de configuración que se creará en el dispositivo del usuario.
Se correrá a la hora de ejecutar el programa, si es que la carpeta no existe previamente.
Empresa: Ocho Fuegos
Autor: Sebastián P. Pincheira
Fecha: 28/01/2024
Lenguaje: Python 3.11.7
Librerías:
- pandas: 2.2.0
"""

# importamos las librerias necesarias
import os
import sys
import shutil
import pandas as pd
import re
from pathlib import Path
import platform

from src.config.universal_variables import controlador_dir as directory

ajustes_dir = directory.parent

# The path to the Configuraciones folder
back_up_variables = os.path.join(directory, "back_up_variables")
variables_folder = os.path.join(directory, "Variables")
source_cod_puerto_destino = os.path.join(back_up_variables, "cod_puerto_destino.json")
destination_cod_puerto_destino = os.path.join(
    variables_folder, "cod_puerto_destino.json"
)
source_precios_contrato = os.path.join(back_up_variables, "precios_contrato.pkl")
destination_precios_contrato = os.path.join(variables_folder, "precios_contrato.xlsx")
source_flete_real = os.path.join(back_up_variables, "flete_real.pkl")
destination_flete_real = os.path.join(variables_folder, "flete_real.xlsx")
source_costo_seco = os.path.join(back_up_variables, "costo_seco.pkl")
destination_costo_seco = os.path.join(variables_folder, "costo_seco.xlsx")


def no_se_encuentran_los_archivos_de_NO_TOCAR() -> bool:
    """
    This function executes an error window signaling that the files were not found. The program stops after the window is closed. Return True if the files were not found.

    Args:
        None

    Returns:
        True if the files were not found. False otherwise.
    """
    if (
        not os.path.exists(source_cod_puerto_destino)
        or not os.path.exists(source_precios_contrato)
        or not os.path.exists(source_flete_real)
    ):
        
        if platform.system() == "Windows":
            os.startfile(ajustes_dir)
        elif platform.system() == "Darwin":  # macOS
            os.system(f'open "{ajustes_dir}"') # HERE
        else:  # Linux and others
            os.system(f'xdg-open "{ajustes_dir}"') # HERE


        import tkinter as tk
        from tkinter import messagebox

        def close_window():
            root.destroy()
            raise SystemExit

        root = tk.Tk()
        root.title("Error")
        root.geometry("400x150")

        error_message = (
            "Los archivos del programa no se encuentran en su totalidad. "
            "Contactar al desarrollador.\nNombre: Sebastián P. Pincheira, "
            "Whatsapp: +56 9 8918 6914, e-mail: sebastian.pincheira@ug.uchile.cl"
        )

        error_label = tk.Label(
            root, text=error_message, padx=20, pady=20, wraplength=350
        )
        error_label.pack()

        ok_button = tk.Button(root, text="OK", width=10, command=close_window)
        ok_button.pack(pady=10)

        root.mainloop()

        return True
    else:
        return False


def make_config():
    """
    Función que crea el archivo de configuración en el dispositivo del usuario si esque falta algo.

    Args:
        None

    Returns:
        None

    Raises:
        AssertionError: Si no se encuentran los archivos de NO_TOCAR
    """
    assert (
        not no_se_encuentran_los_archivos_de_NO_TOCAR()
    ), "Los archivos del programa no se encuentran en su totalidad."

    # Creamos la carpeta de configuración si es que no existe
    if not os.path.exists(variables_folder):
        # Creamos la carpeta de configuración para el usuario
        os.makedirs(variables_folder)
        # Creamos el json para el codigo de puerto destino
        shutil.copy(source_cod_puerto_destino, destination_cod_puerto_destino)
        # Creamos el Excel con los precios de contrato
        precios_contrato_df = pd.read_pickle(source_precios_contrato)
        precios_contrato_df.to_excel(destination_precios_contrato, index=False)
        # Creamos el Excel con el flete real
        flete_real_df = pd.read_pickle(source_flete_real)
        flete_real_df.to_excel(destination_flete_real, index=False)
        # Creamos el Excel de costo seco
        costo_seco_df = pd.read_pickle(source_costo_seco)
        costo_seco_df.to_excel(destination_costo_seco, index=False)
    else:
        # Si falta alguno de los contenidos de la carpeta de configuración, los creamos
        if not os.path.exists(destination_cod_puerto_destino):
            shutil.copy(source_cod_puerto_destino, destination_cod_puerto_destino)
        if not os.path.exists(destination_precios_contrato):
            precios_contrato_df = pd.read_pickle(source_precios_contrato)
            precios_contrato_df.to_excel(destination_precios_contrato, index=False)
        if not os.path.exists(destination_flete_real):
            flete_real_df = pd.read_pickle(source_flete_real)
            flete_real_df.to_excel(destination_flete_real, index=False)
        if not os.path.exists(destination_costo_seco):
            costo_seco_df = pd.read_pickle(source_costo_seco)
            costo_seco_df.to_excel(destination_costo_seco, index=False)
