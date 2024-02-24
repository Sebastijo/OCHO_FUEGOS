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
import json

from src.config.variables import COD_PUERTO_DESTINO

# If you are coding, make sure to change the following directory to the one where you are coding in, the one that contains __main__.py.
coding_directory = r"c:\Users\spinc\Desktop\OCHO_FUEGOS"
# The following will update automatically when running the program. Desired for executable version.
directory = os.path.dirname(os.path.realpath(sys.argv[0]))

# The path to the Configuraciones folder
config_folder = os.path.join(directory, "Configuraciones")

# Creamos la carpeta de configuración si es que no existe
if not os.path.exists(config_folder):
    os.makedirs(config_folder)
# Ponemos el codigo de puerto destino predeterminado si es que no existe otro
if not os.path.exists(os.path.join(config_folder, "cod_puerto_destino.json")):
    with open(os.path.join(config_folder, "cod_puerto_destino.json"), "w") as file:
        json.dump(COD_PUERTO_DESTINO, file)

# Iniciamos la interface de eusuario
from src.frontend.gui_ventas import panqueca
panqueca()

if directory[1:] == coding_directory[1:]:
    import shutil
    shutil.rmtree(config_folder)