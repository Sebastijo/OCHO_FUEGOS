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
if __name__ == "__main__":
    import src.config.variables as var
    from src.frontend.ventana import Ventana
    from src.frontend.buttons import Boton
else:
    from ..config import variables as var
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


def inputErrorWindow(
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
    text_widget = tk.Text(mainFrame_revisar, wrap="none", yscrollcommand=scrollbar.set, width=90)
    text_widget.pack(expand=True, fill=tk.BOTH)
    text_widget.configure(bg=background, fg=foreground, font=("Arial", 12))

    noLeidosHeader = "Embarques no leídos:\n\n"
    text_widget.insert(tk.END, noLeidosHeader)
    embarques_no_leidos = {
        key: ", ".join(f"p. {num}" for num in value)
        for key, value in embarques_no_leidos.items()
        if value != []
    }
    for key, value in embarques_no_leidos.items():
        text_widget.insert(tk.END, "\t" + key + ": " + value + "\n")

    inconsistenciasHeader = "\n Embarques con inconsistencias:\n"
    text_widget.insert(tk.END, inconsistenciasHeader)
    for key in embarques_con_inconsistencias.keys():
        text_widget.insert(tk.END, "\n\t" + str(key[0])+ ", p." + str(key[1]) + "\n")
        for value in embarques_con_inconsistencias[key]:
            text_widget.insert(tk.END, "\t" + "- " + value + "\n")

    text_widget.config(state=tk.DISABLED)
    # Configure the Scrollbar to work with the Text widget
    scrollbar.config(command=text_widget.yview)

    okButton = Boton(mainFrame_revisar, "OK", ventana_revisar.destroy, "output_button")
    okButton.configure(width=10)
    okButton.pack(pady=10)


# Probamos la función revisarWindow
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

    ventana_test = Ventana(titulo="test", ancho=500, alto=500)
    root_test = ventana_test.root
    revisarWindow(root_test, errores, revisar)
    root_test.mainloop()
