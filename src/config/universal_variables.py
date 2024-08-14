"""
Archivo con las variables universales. La idea es llamar desde acá a todas las variables que se necesiten en distintos archivos del programa.
"""

import os
import sys
import re

# Ubicación del programa en el dispositivo del usuario
directory = os.path.dirname(os.path.realpath(sys.argv[0]))
directory = re.sub(r"Controlador\.app/Contents/MacOS$", "", directory) # Cambiar el nombre de "Controlador" por el nombre de la app

print(directory)