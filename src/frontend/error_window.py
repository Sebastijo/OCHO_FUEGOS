"""
Este modulo tiene como objetivo crear una función que despliega una ventana de error si hay un error en el input del usuario.
La función toma la ventana donde se quiere abrir el errorWindow y entrega el valor de verdad de "hay error".
Empresa: Ocho Fuegos
Autor: Sebastián P. Pincheira
Fecha: 10/01/2024
Lenguaje: Python 3.11.7
Librerías:
- tkinter: 8.6.12
"""

# Importamos paquetes
import tkinter as tk

# modulos propios
from ..config import variables as var


# Variables globales
title = var.title
telefono = var.telefono
email = var.email
bg = var.bg
font = var.font
bg_on_enter = var.bg_on_enter

background = bg["window"]


def errorWindow(
    window: tk.Tk,
) -> bool:
    """
    Revisa si se cumplen las condiciones para ejecutar el programa. Si no se cumplen, se ejecuta una ventana de error con la información del error.
    Eventualmente se tiene que agregar otro input a la función para que pueda revisar si se cumplen las condiciones.
    Este otro input posiblemente será el utput de la función contol úbicada en el backend control_final.py.

    Args:
        window (tk.Tk): Ventana principal del programa donde se ejecutará la ventana de error.

    Returns:
        bool: True si se despliega la ventana de error (y no se puede correr el programa), False si no se despliega la ventana de error (y sí se puede correr el programa).
    """

    # Lista de condiciones, si todas son Ture, no se ejecuta el errorWindow. Si una es False, se ejecuta el errorWindow.
    Condicion = [True]  # (Eventualmente) Depende del input de la función

    if not False in Condicion:  # Si no hay errores
        return False  # No se despliega el error window (y se puede correr el programa)

    else:  # Si se detectan errores
        # Lista de mensajes de error, cada uno corresponde a una condición de la lista anterior.
        Outputs = ["<<Mensaje de error a ser presentado en caso de error>>"]
        for i in range(len(Condicion)):  # Revisa cada condición hasta encontrar error
            if (
                Condicion[i] == False
            ):  # La primera condición falsa que encuentra, se despliega en el errorWindow
                say = Outputs[i]

                # Cambios de color de botón al pasar el mouse por encima
                def on_enter_errorButton(event):
                    errorWindowButton["background"] = "#000D56"

                def on_leave_errorButton(event):
                    errorWindowButton["background"] = "#001693"

                # Creación de la ventana de error
                errorWindow = tk.Toplevel(window)
                errorWindow.title("Error")
                errorWindow.config(bg=background)
                errorWindowFrame = tk.Frame(
                    errorWindow, bd=10, relief=tk.GROOVE, bg=background
                )
                errorWindowFrame.pack()
                errorWindowLabel = tk.Frame(errorWindowFrame, bd=5, bg=background)
                errorWindowExit = tk.Frame(errorWindowFrame, bd=10, bg=background)
                errorWindowLabel.pack()
                errorWindowExit.pack()
                errorWindow.title("8Fuegos - Error")
                tk.Label(
                    errorWindowLabel,
                    text=say,
                    wraplength=200,
                    font=30,
                    bg=background,
                    fg="#DDDDDD",
                ).pack()
                errorWindowButton = tk.Button(
                    errorWindowExit,
                    text="OK",
                    font=40,
                    command=errorWindow.destroy,
                    bg="#001693",
                    fg="#FFFFFF",
                    bd=3,
                    width=10,
                    cursor="hand2",
                )
                errorWindowButton.pack()
                errorWindowButton.bind("<Enter>", on_enter_errorButton)
                errorWindowButton.bind("<Leave>", on_leave_errorButton)
                return True  # Se despliega el errorWindow (y no se puede correr el programa)

