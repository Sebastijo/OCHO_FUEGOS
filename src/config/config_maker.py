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

# The following will update automatically when running the program. Desired for executable version.
directory = os.path.dirname(os.path.realpath(sys.argv[0]))

# The path to the Configuraciones folder
config_folder = os.path.join(directory, "config")
source_cod_puerto_destino = (
    r"C:\Users\spinc\Desktop\OCHO_FUEGOS\src\config\cod_puerto_destino.json"
)
destination_cod_puerto_destino = os.path.join(config_folder, "cod_puerto_destino.json")
source_precios_contrato = (
    r"C:\Users\spinc\Desktop\OCHO_FUEGOS\src\config\precios_contrato.pkl"
)
destination_precios_contrato = os.path.join(config_folder, "precios_contrato.xlsx")


def make_config():
    """
    Función que crea el archivo de configuración en el dispositivo del usuario si esque falta algo.

    Args:
        None

    Returns:
        None
    """
    # Creamos la carpeta de configuración si es que no existe
    if not os.path.exists(config_folder):
        # Creamos la carpeta de configuración para el usuario
        os.makedirs(config_folder)
        # Creamos el json para el codigo de puerto destino
        shutil.copy(source_cod_puerto_destino, destination_cod_puerto_destino)
        # Creamos el Excel con los precios de contrato
        precios_contrato_df = pd.read_pickle(source_precios_contrato)
        precios_contrato_df.to_excel(destination_precios_contrato, index=False)
    else:
        # Si falta alguno de los contenidos de la carpeta de configuración, los creamos
        if not os.path.exists(destination_cod_puerto_destino):
            shutil.copy(source_cod_puerto_destino, destination_cod_puerto_destino)
        if not os.path.exists(destination_precios_contrato):
            precios_contrato_df = pd.read_pickle(source_precios_contrato)
            precios_contrato_df.to_excel(destination_precios_contrato, index=False)
