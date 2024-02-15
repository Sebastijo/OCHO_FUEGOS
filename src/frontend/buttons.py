"""
Este modulo tiene como objetivo crear un objeto del tipo boton.
Toma como input el contenedor del boton, el texto del boton y el estilo del boton (ver variables.py).
El boton de información "?" no utiliza este modulo y es una clase por si solo (cf. info_window.py)
Empresa: Ocho Fuegos
Autor: Sebastián P. Pincheira
Fecha: 08/01/2024
Lenguaje: Python 3.11.7
Librerías:
- tkinter: 8.6.12
"""

# Importamos paquetes
import tkinter as tk

# modulos propios
from ..config import variables as var

# Variables universales:
bg = var.bg
bg_on_enter = var.bg_on_enter
fg = var.fg
activebackground = var.activebackground
activeforeground = var.activeforeground
font = var.font


# Creamos la clase Boton que corresponde a los botones que se usarán en el GUI (exceptuando "?", que se definirá directamente cuando se use).
class Boton:
    def __init__(
        self, contenedor: tk.Frame, text: str, command: callable, style: str
    ) -> None:
        """
        Inicializa una instancia de la clase Boton.

        Args:
            contenedor (tk.Frame): Frame o ventana donde se creará el widget.
            text (str): Texto que aparecerá en el botón.
            command (callable): Función que se ejecutará al presionar el botón.
            style (str): Estilo del botón. Puede ser "output_button" o "exit_button".

        Returns:
            None

        Raises:
            AssertionError: Si el estilo no es "output_button" o "exit_button".
        """

        assert style in (
            "output_button",
            "exit_button",
        ), "El estilo del botón debe ser 'output_button' o 'exit_button'."

        # Crear el botón
        self.style = style
        self.boton = tk.Button(
            contenedor,
            text=text,
            command=command,
            font=var.font[style],
            bg=var.bg[style],
            fg=var.fg[style],
            activebackground=var.activebackground[style],
            activeforeground=var.activeforeground[style],
            bd=3,
            relief=tk.RAISED,
            cursor="hand2",
        )

        self.boton.bind(
            "<Enter>",
            lambda event: (
                self.boton.config(bg=bg_on_enter["output_button"])
                if self.style == "output_button"
                else (
                    self.boton.config(bg=bg_on_enter["exit_button"])
                    if self.style == "exit_button"
                    else None
                )
            ),
        )

        # Oscurecer boton al entrar a él
        self.boton.bind(
            "<Enter>", lambda event: self.boton.config(bg=bg_on_enter[self.style])
        )
        # Aclarar boton al salir de él
        self.boton.bind("<Leave>", lambda event: self.boton.config(bg=bg[self.style]))

    def pack(self, **kwargs):
        """
        Empaqueta el botón en el contenedor.

        Args:
            **kwargs: Argumentos de empaquetado.

        Returns:
            None
        """
        self.boton.pack(**kwargs)

    def grid(self, **kwargs):
        """
        Ubica el botón en el contenedor.

        Args:
            **kwargs: Argumentos de ubicación.

        Returns:
            None
        """
        self.boton.grid(**kwargs)

    def place(self, **kwargs):
        """
        Ubica el botón en el contenedor.

        Args:
            **kwargs: Argumentos de ubicación.

        Returns:

        """
        self.boton.place(**kwargs)

    def bind(self, *args, **kwargs):
        """
         Asocia eventos con funciones de devolución de llamada específicas

        Args:
            **kwargs: Argumentos de la función bind.

        Returns:

        """
        self.boton.bind(*args, **kwargs)

    def configure(self, **kwargs):
        """
        Configura una nueva propiedad para el botón.

        Args:
            **kwargs: Argumentos de configuración.

        Returns:

        """
        self.boton.configure(**kwargs)

    def destroy(self):
        """
        Destruye el botón.

        Returns:

        """
        self.boton.destroy()

    def disable(self):
        """
        Deshabilita el botón.

        Returns:

        """
        self.boton.config(state="disabled")

    def enable(self):
        """
        Habilita el botón.

        Returns:

        """
        self.boton.config(state="normal")
