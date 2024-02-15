import tkinter as tk
from tkinter import ttk
import time
import threading
from tkinterdnd2 import *
from src.backend.control_final import control
import sys

embarques_path_ = (
        r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\mock_base_embarques.xlsx"
    )
facturas_path_ = (
    r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\mock_facturas_proformas.xlsx"
    )
tarifa_path_ = r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\mock_tarifa_aerea.xlsx"

liquidaciones_path_ = r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\mock_liquidacion"


def salir():
    thread = threader[0]
    thread.join()
    root.destroy()
    sys.exit()

def process():
    control(embarques_path_, facturas_path_, tarifa_path_, liquidaciones_path_)

threader = []

def process_thread():
    progress_bar.start()
    thread = threading.Thread(target=process)
    thread.start()
    threader.clear()
    threader.append(thread)

# GUI setup
root = TkinterDnD.Tk()
root.title("Loading Bar GUI")

# Create and place widgets
frame = ttk.Frame(root, padding="10")
frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

button_ejecutar = ttk.Button(frame, text="Ejecutar", command=process_thread)
button_ejecutar.grid(column=0, row=0, pady=10)

button_salir = ttk.Button(frame, text="Salir", command=salir)
button_salir.grid(column=1, row=0, pady=10)

progress_bar = ttk.Progressbar(frame, mode="indeterminate", length=200)
progress_bar.grid(column=0, row=1, columnspan=2, pady=10)


root.mainloop()