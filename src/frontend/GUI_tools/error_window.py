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
import pickle as pkl

# modulos propios
from . import GUI_variables as var
from .ventana import Ventana
from .buttons import Boton


# Variables globales
title = var.title
telefono = var.telefono
email = var.email
bg = var.bg
font = var.font
bg_on_enter = var.bg_on_enter
fg = var.fg

background = bg["window"]
foreground = fg["window"]


def inputErrorWindow(window: tk.Tk, e: Exception):
    """
    Crea una ventana sobre window explicando la excepción e.

    Args:
        window (tk.Tk): Ventana principal del programa donde se ejecutará la ventana de error.
        e (Exception): Excepción que se quiere mostrar en la ventana de error.

    Returns:
        None
    """
    ventana_error = Ventana(titulo="8Fuegos - Error", padre=window)
    mainFrame_error = ventana_error.mainFrame

    label_error_header = tk.Label(
        mainFrame_error,
        text="No se pudo ejecutar el programa a causa del siguiente error:\n",
        bg=background,
        fg=foreground,
        font=font,
    )
    label_error = tk.Label(
        mainFrame_error, text=str(e), bg=background, fg=foreground, font=font
    )
    label_error_header.pack(padx=30, pady=(30, 10))
    label_error.pack(padx=10, pady=(0, 30))

    okButton = Boton(mainFrame_error, "OK", ventana_error.destroy, "output_button")
    okButton.pack(pady=10)


def revisarWindow(
    window: tk.Tk, embarques_no_leidos: dict, embarques_con_inconsistencias: dict
):
    """
    Despliega una ventana con los errores que debe revisar el usuario.

    Args:
        window (tk.Tk): Ventana principal del programa donde se ejecutará la ventana de error.
        embarques_no_leidos (dict): Diccionario con los embarques que no se pudieron leer.
        embarques_con_inconsistencias (dict): Lista con los embarques que tienen inconsistencias.

    Returns:
        None
    """
    ventana_revisar = Ventana(titulo="8Fuegos - Reporte de errores", padre=window)
    root_revisar = ventana_revisar.root
    mainFrame_revisar = ventana_revisar.mainFrame

    # Create a Scrollbar
    scrollbar = tk.Scrollbar(mainFrame_revisar)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Create a Text widget and attach the Scrollbar
    text_widget = tk.Text(
        mainFrame_revisar, wrap="none", yscrollcommand=scrollbar.set, width=90
    )
    text_widget.pack(expand=True, fill=tk.BOTH)
    text_widget.configure(bg=background, fg=foreground, font=font)

    # Creamos el forrmato y agregamos los embarques no leídos
    noLeidosHeader = "Embarques no leídos:\n\n"
    text_widget.insert(tk.END, noLeidosHeader)
    embarques_no_leidos = {
        key: ", ".join(f"p. {num}" if type(num) != str else f"{num}" for num in value)
        for key, value in embarques_no_leidos.items()
        if value != []
    }
    for key, value in embarques_no_leidos.items():
        text_widget.insert(tk.END, "\t" + key + ": " + value + "\n")

    # Creamos el formato y agregamos los embarques con inconsistencias
    inconsistenciasHeader = "\n Embarques con inconsistencias:\n"
    text_widget.insert(tk.END, inconsistenciasHeader)
    for key in embarques_con_inconsistencias.keys():
        text_widget.insert(tk.END, "\n\t" + str(key[0]) + ", p." + str(key[1]) + "\n")
        for value in embarques_con_inconsistencias[key]:
            text_widget.insert(tk.END, "\t" + "- " + value + "\n")

    text_widget.config(state=tk.DISABLED)
    # Configure the Scrollbar to work with the Text widget
    scrollbar.config(command=text_widget.yview)

    okButton = Boton(mainFrame_revisar, "OK", ventana_revisar.destroy, "output_button")
    okButton.pack(pady=10)


# Probamos la función revisarWindow y inputErrorWindow
if __name__ == "__main__":
    errores_pickle = (
        r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\pickles\errores.pkl"
    )
    revisar_pickle = (
        r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\pickles\revisar.pkl"
    )
    with open(errores_pickle, "rb") as file:
        # Load the dictionary from the Pickle file
        errores = pkl.load(file)
    with open(revisar_pickle, "rb") as file:
        # Load the dictionary from the Pickle file
        revisar = pkl.load(file)
    e = ValueError("Test error")

    ventana_test = Ventana(titulo="test")
    root_test = ventana_test.root
    mainFrame_test = ventana_test.mainFrame
    revisar_button = Boton(
        mainFrame_test,
        "Revisar",
        lambda: revisarWindow(root_test, errores, revisar),
        "output_button",
    )
    error_button = Boton(
        mainFrame_test, "Error", lambda: inputErrorWindow(root_test, e), "output_button"
    )
    salir_button = Boton(mainFrame_test, "Salir", ventana_test.destroy, "exit_button")
    revisar_button.pack()
    error_button.pack()
    salir_button.pack()

    mainFrame_test.mainloop()
