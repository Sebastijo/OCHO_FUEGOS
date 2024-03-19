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

if __name__ == "__main__":
    from src.config import variables as var
else:
    from . import variables as var

directory = var.directory

# The path to the Configuraciones folder
datos_folder = os.path.join(directory, "Datos del programa")
NO_TOCAR_folder = os.path.join(datos_folder, "NO TOCAR")
variables_folder = os.path.join(datos_folder, "Variables")
source_cod_puerto_destino = os.path.join(NO_TOCAR_folder, "cod_puerto_destino.json")
destination_cod_puerto_destino = os.path.join(
    variables_folder, "cod_puerto_destino.json"
)
source_precios_contrato = os.path.join(NO_TOCAR_folder, "precios_contrato.pkl")
destination_precios_contrato = os.path.join(variables_folder, "precios_contrato.xlsx")


def make_config():
    """
    Función que crea el archivo de configuración en el dispositivo del usuario si esque falta algo.

    Args:
        None

    Returns:
        None
    """
    # Creamos la carpeta de configuración si es que no existe
    if not os.path.exists(variables_folder):
        # Creamos la carpeta de configuración para el usuario
        os.makedirs(variables_folder)
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

if __name__ == "__main__":
    make_config()