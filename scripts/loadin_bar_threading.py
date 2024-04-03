"""
El objetivo de este mòdulo es aislar el problema de la carga de la barra de progreso en un hilo separado.
"""

import tkinter as tk
from tkinter import ttk
import threading
import time

import shutil
import os
destination_datos_del_programa = (
    r"C:\\Users\\spinc\\Desktop\\OCHO_FUEGOS\\scripts\\Datos del programa"
)
source_datos_del_programa = r"C:\Users\spinc\Desktop\OCHO_FUEGOS\Datos del programa"
if not os.path.exists(destination_datos_del_programa):
    shutil.copytree(source_datos_del_programa, destination_datos_del_programa)

from src.config import variables as var
from src.backend.embarques import pseudoControl
from src.backend.liquidacion_reader import liquidaciones

embarques = r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\Base embarques.xlsx"
facturas = r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\Facturas proformas.xlsx"
tarifas = r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\Tarifas.xlsx"
liquidacion_folder = r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\Liquidaciones"


def my_function():

    pseudoControl(embarques, facturas, tarifas)
    liquidaciones(liquidacion_folder)
    shutil.rmtree(destination_datos_del_programa)

    # Updating GUI after process finishes
    root.event_generate("<<ProcessFinished>>", when="tail")


def run_function():
    # Disable button during execution
    ejecutar_button.config(state="disabled")
    # Show loading bar
    progress_bar.start()
    # Run function in a separate thread to avoid freezing GUI
    threading.Thread(target=my_function).start()


def on_process_finished(event):
    # Stop loading bar
    progress_bar.stop()
    # Enable button
    ejecutar_button.config(state="normal")
    # Update label text
    status_label.config(text="The process has finished successfully")


# Create main window
root = tk.Tk()
root.title("Insanely GUI")

# Set window width and height
window_width = 350
window_height = 150
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Create button
ejecutar_button = tk.Button(root, text="Ejecutar", command=run_function)
ejecutar_button.pack(pady=10)

# Create progress bar
progress_bar = ttk.Progressbar(root, mode="indeterminate", length=300)
progress_bar.pack(pady=10)

# Create label for status message
status_label = tk.Label(root, text="")
status_label.pack(pady=10)

# Bind event for process finished
root.bind("<<ProcessFinished>>", on_process_finished)

# Start GUI main loop
root.mainloop()
