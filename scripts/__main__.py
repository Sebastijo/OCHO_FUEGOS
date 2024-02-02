"""
Automatisación de procesos corporativos: registro de gastos y ganacnias de la empresa.
El siguiente programa tiene como objetivo recibir archivos de Excel (a veces en formato PDF) y generar un reporte de gastos y ganancias de la empresa con detalles.
Empresa: Ocho Fuegos
Autor: Sebastián P. Pincheira
Fecha: 03/01/2024
Versión: 0.1.0
Lenguaje: Python 3.12.0
Librerías:
- pandas: 1.5.3
- matplotlib: 3.8.0
- pdf_to_excel (tabula: 2.6.0)
"""

__version__ = "0.1.0"

# Importar librerías
import pandas as pd
import matplotlib as plt
from src.backend import liquidacion_reader
from src.frontend.file_select import BarraBusqueda

import tkinter.filedialog
import tkinter as tk
from tkinterdnd2 import *


# Crear la ventana principal de la aplicación
root = TkinterDnD.Tk()
root.title("Obtener ruta del archivo")

barraBusqueda = BarraBusqueda(root)
barraBusqueda.pack()

# Iniciar el bucle principal de la aplicación
root.mainloop()
