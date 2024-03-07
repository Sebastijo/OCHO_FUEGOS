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
import sys

from src.config import variables as var

directory = var.directory

# Obtenemos los paths que deben existir antes de correr el programa
config_folder = os.path.join(directory, "config")
destination_cod_puerto_destino = os.path.join(config_folder, "cod_puerto_destino.json")
destination_precios_contrato = os.path.join(config_folder, "precios_contrato.xlsx")
output_folder = os.path.join(directory, "output")

config_paths = [
    config_folder,
    destination_cod_puerto_destino,
    destination_precios_contrato,
]

if not all([os.path.exists(path) for path in config_paths]):
    # Creamos las carpeta de configuración en el dispositivo del usuario
    from src.config.config_maker import make_config

    make_config()

# Creamos la carpeta de output en el dispositivo del usuario, de no existir.
if not os.path.exists(output_folder):
    os.mkdir(output_folder)


# Iniciamos la interface de eusuario
from src.frontend.gui_ventas import panqueca

panqueca()


# If you are coding, make sure to change the following directory to the one where you are coding in, the one that contains __main__.py.
coding_directory = r"c:\Users\spinc\Desktop\OCHO_FUEGOS"
# The following will update automatically when running the program. Desired for executable version.
directory = os.path.dirname(os.path.realpath(sys.argv[0]))

if directory[1:] == coding_directory[1:]:
    import shutil

    shutil.rmtree(config_folder)
