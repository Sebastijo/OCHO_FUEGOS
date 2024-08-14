# Importación de bibliotecas necesarias
import tkinter as tk
from tkinter import ttk
from tkinterdnd2 import *
import pandas as pd
from xlsxwriter.workbook import Workbook
import os

# import sys
# import threading

import shutil
import os
destination_datos_del_programa = (
    r"C:\\Users\\spinc\\Desktop\\OCHO_FUEGOS\\scripts\\Datos del programa"
)
source_datos_del_programa = r"C:\Users\spinc\Desktop\OCHO_FUEGOS\Datos del programa"
if not os.path.exists(destination_datos_del_programa):
    shutil.copytree(source_datos_del_programa, destination_datos_del_programa)

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

# Variables universales:
bg = var.bg  # Color de fondo
fg = var.fg  # Color de texto
title = var.title  # Título de la ventana principal
directory = var.directory  # Directorio de trabajo

datos_folder = os.path.join(directory, "Datos del programa")
control_path = os.path.join(
    datos_folder, "output", "Control.xlsx"
)  # Path del control

def initial_window() -> tuple[tk.Tk, tk.Frame, dict]:
    """
    Función que crea la ventana inicial de la GUI de ventas.

    Args:
        None

    Returns:
        root: Ventana principal de la GUI.
        mainFrame: Marco principal de la GUI.
        barrasBusqueda: Diccionario con las barras de búsqueda de archivos.
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

    # Creación de los botones finales de output y de exit.
    frameFinalButtonsAndBar = tk.Frame(mainFrame, bd=4, bg=bg["window"])
    frameFinalButtons = tk.Frame(frameFinalButtonsAndBar, bd=4, bg=bg["window"])
    info = InfoBoton(
        frameFinalButtons,
        """
        Este programa te permite gestionar información crucial de embarques, facturas, tarifas y liquidaciones mediante una práctica base de formato Excel. Sigue estos simples pasos:

        1. Configuración Inicial:
        - Dirígete a la ubicación del programa en tu dispositivo y asegúrate de que la carpeta 'config' contenga los archivos esperados.
        - Puedes ajustar los contenidos de la carpeta 'config' según tus necesidades. No cambies el formato, solo los contenidos (añadir filas al Excel, palabras al diccionario, etc.).
        - Si la carpeta 'config' se corrompe, bórrala y vuelve a ejecutar el programa para restablecerla con los valores predeterminados.

        2. Cargar Archivos:
        - Arrastra tus archivos a las áreas correspondientes en el menú principal.
        - La barra para subir liquidaciones acepta formatos como Excel, PDF o una carpeta que contenga estos documentos.
        - Formatos de liquidaciones admitidos: 12Islands (.pdf), JumboFruit (comienza con 'BQ'), Happy Farm Fruit (comienza con 'HFF'), y formato estándar (comienza con '8F').
        - Presiona 'Ejecutar' después de cargar tus archivos y espera a que el programa los procese.

        3. Resultados:
        - Una vez completado, encontrarás el resultado en la carpeta 'outputs' junto con un informe de errores en esta interfaz.
        - El informe incluye liquidaciones no leídas y embarques con inconsistencias.
        - Liquidaciones no leídas: errores de formato en el input.
        - Inconsistencias en liquidaciones: problemas en el contenido (por ejemplo, comisiones incorrectas).

        4. Salida Final:
        - La carpeta 'outputs' contendrá un Excel con tres hojas: Base de Control, Liquidaciones no Pareadas y No Vendidos.
        - Liquidaciones no pareadas: no asociadas a ningún embarque de la base de embarques.
        - No vendidos: embarques cuyas unidades se venden a $0 USD.

        5. Soporte y Contacto:
        - Para agregar un nuevo formato, actualizar el programa o para cualquier necesidad adjacente a la ingeniería o a la ingeniería matemática, no dude en contactar al desarrollador (datos disponibles al final de esta ventana).
        """,
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
    # ejecutar.configure(command=runVentas)

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

    return root, mainFrame, barrasBusqueda, frameFinalButtonsAndBar
    
    
initial_window()


shutil.rmtree(destination_datos_del_programa)