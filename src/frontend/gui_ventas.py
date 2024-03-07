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
- pandas: 2.2.0
"""

# Importación de bibliotecas necesarias
import tkinter as tk
from tkinter import ttk
from tkinterdnd2 import *
import pandas as pd
from xlsxwriter.workbook import Workbook
import os

# import sys
# import threading

# modulos propios
if __name__ == "__main__":
    from src.frontend.file_select import BarraBusqueda
    from src.frontend.buttons import Boton
    import src.config.variables as var
    from src.frontend.info_window import InfoBoton
    from src.frontend.error_window import inputErrorWindow, revisarWindow
    from src.backend.control_final import control
    from src.frontend.ventana import Ventana
    from src.backend.output_doc_maker import export
else:
    from .file_select import BarraBusqueda
    from .buttons import Boton
    from ..config import variables as var
    from .info_window import InfoBoton
    from .error_window import inputErrorWindow, revisarWindow
    from ..backend.control_final import control
    from .ventana import Ventana
    from ..backend.output_doc_maker import export

    # Variables universales:
    bg = var.bg  # Color de fondo
    fg = var.fg  # Color de texto
    title = var.title  # Título de la ventana principal
    control_path = var.output_directory_path  # Path del archivo de control


def panqueca():
    """
    Función que corre el GUI de ventas. Genera el xls de control.

    Args:
        None

    Returns:
        None

    Raises:
        None
    """

    # Creación de la ventana principal utilizando tkinter
    ventana = Ventana(titulo=title["main"], DnD=True)
    root = ventana.root
    mainFrame = ventana.mainFrame

    frameBusquedas = tk.Frame(mainFrame, bd=4, relief=tk.FLAT, bg=bg["window"])
    frameBusquedas.grid(row=0, column=0)

    # Creación de los widgets de búsqueda de archivos
    contents = {
        "embarques": "Seleccione un archivo .xls de embarques",
        "facturas": "Seleccione un archivo .xls de facturas",
        "tarifas": "Seleccione un archivo .xls de tarifas",
        "liquidaciones": "Seleccione una carpeta con liquidaciones de 12Islands",
    }
    barrasBusqueda = {}  # Lista que contiene las barras de busqueda
    for idx, tipo in enumerate(contents):
        barrasBusqueda[tipo] = BarraBusqueda(frameBusquedas, contents[tipo])
        # Creamos la barra de busqueda con el contenido descrito
        barrasBusqueda[tipo].grid(
            row=idx, column=0
        )  # Montamos la barra de busqueda en el frame

    # Acción del botón de ejecución
    def runVentas() -> None:
        """
        Función que se ejecuta al presionar el botón de ejecución.
        """
        ejecutar.disable()
        # Guardamos los paths de los archivos seleccionados
        inputPaths = (
            {}
        )  # Diccionario que contiene los paths de los archivos seleccionados
        for tipo in barrasBusqueda:
            inputPaths[tipo] = (
                barrasBusqueda[tipo].get("1.0", "end-1c").replace("/", "\\")
            )

        # Ejecutamos el programa de ventas
        try:
            control_df, errores, revisar, liquidaciones_no_pareadas, no_vendidos = (
                control(
                    inputPaths["embarques"],
                    inputPaths["facturas"],
                    inputPaths["tarifas"],
                    inputPaths["liquidaciones"],
                )
            )
        except Exception as e:
            inputErrorWindow(root, e)
            ejecutar.enable()
            return

        # Verificamos error y, a la vez, mostramos errorWindow en caso de haber.
        frameFinalButtonsAndBar.grid_forget()  # Borramos los botones finales

        # Exportamos los resultados a la carpeta de outputs
        export(control_df, liquidaciones_no_pareadas, no_vendidos)

        # Cambiamos el texto de los outputs
        output[0].configure(
            text=f"El resultado se encuentra disponible en\r {control_path}"
        )
        num_errores = sum(len(definition) for definition in errores.values())
        num_revisar = len(revisar)
        if num_errores + num_revisar == 0:
            output[1].configure(text="No se detectaron errores en la ejecución")
        else:
            output[1].configure(
                text=f"Hubo {num_errores} embarques cuya liquidación no se pudo leer\r y {num_revisar} embarques cuyas liquidaciones tienen inconsistencias"
            )
            output[-1].pack(padx=10, pady=(10, 10))
            output[-1].configure(command=lambda: revisarWindow(root, errores, revisar))
        outputFrame.grid(row=1, column=0)  # Mostramos el frame de los outputs
        frameFinalButtonsAndBar.grid(
            row=2, column=0, sticky=tk.E
        )  # Mostramos los botones finales
        ejecutar.enable()  # Habilitamos el botón de ejecución
        # loading_bar.stop()  # Detenemos la barra de progreso
        # loading_bar.pack_forget()  # Ocultamos la barra de progreso
        return

    # Creamos el contenido de los outputs:
    outputFrame = tk.Frame(
        mainFrame, bg=bg["window"], width=500, height=70, bd=5, relief=tk.SUNKEN
    )
    output = []
    for i in range(2):
        output.append(
            tk.Label(outputFrame, width=81, bg=bg["window_text"], fg=fg["window_text"])
        )
        output[i].pack()
    output.append(
        Boton(
            outputFrame,
            "Reporte de errores",
            lambda: print("por revisar:"),
            "output_button",
        )
    )

    # Creación de los botones finales de output y de exit.
    frameFinalButtonsAndBar = tk.Frame(mainFrame, bd=4, bg=bg["window"])
    frameFinalButtons = tk.Frame(frameFinalButtonsAndBar, bd=4, bg=bg["window"])
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

    # Boton que cierra el programa, eliminando los threads abiertos
    def quitter():
        # for thread in threading.enumerate():
        #    if thread != threading.main_thread():
        #        thread.join()
        root.quit()

    salir = Boton(frameFinalButtons, "Salir", quitter, "exit_button")
    # Create and configure the progress bar
    style = ttk.Style()
    style.configure("TProgressbar", thickness=20)
    # loading_bar = ttk.Progressbar(
    #    frameFinalButtonsAndBar, mode="indeterminate", style="TProgressbar", length=450
    # )

    """
    def update_loading_bar(progress):

        Función que actualiza la barra de progreso.

        return
    """

    # threader = []

    """
    def runVentas_thread():
        
        Función que ejecuta la función runVentas en un hilo.
        
        ejecutar.disable()
        loading_bar.start()
        loading_bar.pack()
        thread = threading.Thread(target=runVentas, daemon=True)
        thread.start()
        threader.clear()
        threader.append(thread)
    """

    # Hacer una función que una los threads y cierre la GUI. !!!!!

    # Definimos el command del boton ejecutar
    ejecutar.configure(command=runVentas)

    # Cargamos los botones a la ventana
    frameFinalButtonsAndBar.grid(row=1, column=0, sticky=tk.E)
    frameFinalButtons.pack(side=tk.RIGHT, anchor="n")

    # loading_bar.pack(side=tk.LEFT, padx=10, pady=0)
    # loading_bar.pack_forget()
    info.pack(side=tk.LEFT, anchor="n")
    salir.pack(side=tk.RIGHT, anchor="n")
    ejecutar.pack(side=tk.RIGHT, anchor="n")

    # Inicio del bucle principal para la ejecución de la interfaz gráfica
    root.mainloop()
