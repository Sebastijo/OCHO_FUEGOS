"""
Interface de usuario gráfica para el programa de automatisación de procesos corporativos, sección de ventas.
El objetivo del siguiente programa es crear una GUI a partir de tkinter para el programa de automatisación de procesos corporativos.
Empresa: Ocho Fuegos
Autor: Sebastián P. Pincheira
Fecha: 03/01/2024
Lenguaje: Python 3.11.7
Librerías:
- tkinter: 8.6.12
- tkinterdnd2: 0.2.1
"""

# Importación de bibliotecas necesarias
import tkinter as tk
from tkinterdnd2 import *

# modulos propios
if __name__ == "__main__":
    from src.frontend.file_select import BarraBusqueda
    from src.frontend.buttons import Boton
    import src.config.variables as var
    from src.frontend.info_window import InfoBoton
    from src.frontend.error_window import errorWindow
else:
    from .file_select import BarraBusqueda
    from .buttons import Boton
    from ..config import variables as var
    from .info_window import InfoBoton
    from .error_window import errorWindow

# Variables universales:
bg = var.bg  # Color de fondo
fg = var.fg  # Color de texto
title = var.title  # Título de la ventana principal

# Creación de la ventana principal utilizando tkinter
root = TkinterDnD.Tk()

root.config(bg=bg["window"])

# Establecimiento del título de la ventana principal
root.title(title["main"])

# Creación del marco principal con propiedades específicas
mainFrame = tk.Frame(root, bd=10, relief=tk.GROOVE, bg=bg["window"])
mainFrame.pack()

frameBusquedas = tk.Frame(mainFrame, bd=4, relief=tk.FLAT, bg=bg["window"])
frameBusquedas.grid(row=0, column=0)

# Creación de los widgets de búsqueda de archivos
contents = ("embarques", "facturas", "tarifas")
barraBusqueda = []  # Lista que contiene las barras de busqueda
for i in range(3):
    barraBusqueda.append(
        BarraBusqueda(frameBusquedas, contents[i])
    )  # Creamos la barra de busqueda con el contenido descrito
    barraBusqueda[i].grid(row=i, column=0)  # Montamos la barra de busqueda en el frame


# Acción del botón de ejecución
def runVentas() -> dict:
    """
    Función que se ejecuta al presionar el botón de ejecución.
    """
    # Guardamos los paths de los archivos seleccionados
    inputPaths = {}  # Diccionario que contiene los paths de los archivos seleccionados
    for i in range(3):
        inputPaths[contents[i]] = barraBusqueda[i].get("1.0", "end-1c")
    
    # Ejecutamos el programa de ventas
    # control_de_embarques = <<PROGRAMA>>(embarques, facturas, tarifas) # Por definir en el backend
    if not errorWindow(root): # Verificamos error y, a la vez, mostramos errorWindow en caso de haber.
        frameFinalButtons.grid_forget()  # Borramos los botones finales
        # Cambiamos el texto de los outputs
        output[0].configure(text="El resultado se encuentra disponible en")
        output[1].configure(text="<<PATH>>")
        output[2].configure(text="Dato: foo")
        outputFrame.grid(row=1, column=0)  # Mostramos el frame de los outputs
        frameFinalButtons.grid(
            row=2, column=0, sticky=tk.E
        )  # Mostramos los botones finales
        return
    else: # Se detectan errores
        return


# Creamos el contenido de los outputs:
outputFrame = tk.Frame(
    mainFrame, bg=bg["window"], width=500, height=70, bd=5, relief=tk.SUNKEN
)
output = []
for i in range(3):
    output.append(
        tk.Label(outputFrame, width=81, bg=bg["window_text"], fg=fg["window_text"])
    )
    output[i].pack()


# Creación de los botones finales de output y de exit.
frameFinalButtons = tk.Frame(mainFrame, bd=4, bg=bg["window"])
info = InfoBoton(
    frameFinalButtons,
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean euismod bibendum laoreet."
    + " Proin gravida dolor sit amet lacus accumsan et viverra justo commodo."
    + " Proin sodales pulvinar tempor. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus."
    + " Nam fermentum, nulla luctus pharetra vulputate,"
    + " Felis tellus mollis orci, sed rhoncus sapien nunc eget odio. Lorem ipsum dolor sit amet, consectetur adipiscing elit."
    + " Aenean euismod bibendum laoreet. Proin gravida.",
)  # Boton de información sobre el programa
ejecutar = Boton(
    frameFinalButtons, "Ejecutar", lambda: print("Ejecutar"), "output_button"
)  # Botón de ejecución
salir = Boton(frameFinalButtons, "Salir", root.quit, "exit_button")  # Botón de salida


# Definimos el command del boton ejecutar
ejecutar.configure(command=runVentas)

# Cargamos los botones a la ventana
frameFinalButtons.grid(row=1, column=0, sticky=tk.E)

info.pack(side=tk.LEFT, anchor="n")
salir.pack(side=tk.RIGHT, anchor="n")
ejecutar.pack(side=tk.RIGHT, anchor="n")


# Inicio del bucle principal para la ejecución de la interfaz gráfica
root.mainloop()
