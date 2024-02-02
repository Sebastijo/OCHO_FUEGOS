"""
El objetivo de este modulo es crear una clase que consiste en un boton que al clickearlo, se ejecuta una ventana con información sobre el programa.
El objeto recibe como parametros el contenedor donde se creará el widget y el texto que aparecerá en el botón.
Empresa: Ocho Fuegos
Autor: Sebastián P. Pincheira
Fecha: 09/01/2024
Lenguaje: Python 3.11.7
Librerías:
- tkinter: 8.6.12
"""

# Importamos paquetes
import tkinter as tk
import tkinter.font as tkfont

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


def infoWindow(info: str, window: tk.Tk) -> None:
    """
    Crea una ventana con información sobre el programa.

    Args:
        info (str): Texto que aparecerá en la ventana.
        window (tk.Tk): Ventana padre.

    Returns:
        None
    """

    def on_enter_errorButton(e):
        errorWindowButton["background"] = "#000D56"

    def on_leave_errorButton(e):
        errorWindowButton["background"] = "#001693"

    say = info
    errorWindow = tk.Toplevel(window)
    errorWindow.config(bg=background)
    errorWindow.title(title["info1"])
    errorWindowFrame = tk.Frame(
        errorWindow, bd=10, relief=tk.GROOVE, bg=background, width=300
    )
    exitFrame = tk.Frame(errorWindowFrame, bd=10, bg=background, width=300)
    datosFrame = tk.Frame(exitFrame, bd=10, bg=background, width=100)
    errorWindowFrame.pack()
    errorWindowLabel = tk.Frame(errorWindowFrame, bd=5, bg=background, width=300)
    datosLabel1 = tk.Label(
        datosFrame, text="Sebastián P. Pincheira", bg=background, fg="#DDDDDD", bd=0
    )
    datosLabel1_ = tk.Label(
        datosFrame,
        text="Estudiante Ingeniería Civil Matemática",
        bg=background,
        fg="#DDDDDD",
        bd=0,
    )
    datosLabel2 = tk.Label(
        datosFrame, text=telefono + " (WhatsApp)", bg=background, fg="#DDDDDD", bd=0
    )
    datosLabel3 = tk.Label(
        datosFrame, text=email, bg=background, fg="#DDDDDD", bd=0
    )
    ESPACIOXD = tk.Label(exitFrame, text="asdasdasdasdasdasdasdas", bg=background, fg=background)
    # errorWindowExit   = tk.Frame(exitFrame, bd=10, bg = background)
    errorWindowLabel.pack()
    datosFrame.grid(column=1, row=1)
    ESPACIOXD.grid(column=2, row=1)
    datosLabel1.pack(anchor=tk.W)
    datosLabel1_.pack(anchor=tk.W)
    datosLabel2.pack(anchor=tk.W)
    datosLabel3.pack(anchor=tk.W)
    # errorWindowExit.pack()
    tk.Label(
        errorWindowLabel, text=say, wraplength=800, font=30, bg=background, fg="#DDDDDD"
    ).pack()

    exitFrame.pack(anchor=tk.W)
    errorWindowButton = tk.Button(
        exitFrame,
        text="OK",
        font=40,
        command=errorWindow.destroy,
        bg="#001693",
        fg="#FFFFFF",
        bd=3,
        width=10,
        cursor="hand2",
    )
    errorWindowButton.grid(column=3, row=1)
    errorWindowButton.bind("<Enter>", on_enter_errorButton)
    errorWindowButton.bind("<Leave>", on_leave_errorButton)


class InfoBoton:
    """
    Clase que representa un botón de información. Al clickearlo, se ejecuta una ventana con información sobre el programa.
    """

    def __init__(self, contenedor: tk.Frame, info: str) -> None:
        """
        Inicializa una instancia de la clase Info.

        Args:
            contenedor (tk.Frame): Frame o ventana donde se creará el widget.
            info (str): Texto que aparecerá en el botón.

        Returns:
            None
        """
        self.info = info
        self.boton = tk.Button(
            contenedor,
            text="?",
            width=1,
            relief=tk.RAISED,
            command=lambda: infoWindow(self.info, self.boton.winfo_toplevel()),
            cursor="hand2",
        )
        self.boton["font"] = tkfont.Font(size=font["?"])
        self.boton.bind("<Enter>", lambda event: self.boton.config(bg=bg_on_enter["?"]))
        self.boton.bind("<Leave>", lambda event: self.boton.config(bg=bg["?"]))

    def grid(self, **kwargs) -> None:
        """
        Empaqueta el botón en un grid.

        Returns:
            None
        """
        self.boton.grid(**kwargs)

    def pack(self, **kwargs) -> None:
        """
        Empaqueta el botón en un pack.

        Returns:
            None
        """
        self.boton.pack(**kwargs)

    def place(self, **kwargs) -> None:
        """
        Empaqueta el botón en un place.

        Returns:
            None
        """
        self.boton.place(**kwargs)
