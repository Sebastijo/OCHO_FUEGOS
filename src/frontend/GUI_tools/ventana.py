"""
El objetivo de este modulo es crear una ventana genérica que será utilizada en todas las ventanas del programa. Esto se realizará mediante la creación de una clase.
Empresa: Ocho Fuegos
Autor: Sebastián P. Pincheira
Fecha: 01/02/2024
Lenguaje: Python 3.11.7
Librerías:
- tkinter: 8.6.12
"""

# Importamos paquetes
import tkinter as tk
from tkinterdnd2 import *

# Importamos paquetes propios
from . import GUI_variables as var

bg = var.bg
fg = var.fg


class Ventana:
    def __init__(self, titulo="", ancho=0, alto=0, padre=False, DnD=False) -> None:
        """
        Inicializa una instancia de la clase Ventana.

        Args:
            titulo (str): Título de la ventana.
            ancho (int): Ancho de la ventana.
            alto (int): Alto de la ventana.
            padre (tk.Tk or TkinterDnD.Tk, optional): Ventana padre. Defaults to False.
            DnD (bool, optional): Habilita o deshabilita el Drag and Drop. Defaults to False.


        Returns:
            None

        Raises:
            AssertionError: Si el título no es un string.
            AssertionError: Si el ancho no es un entero.
            AssertionError: Si el alto no es un entero.
            AssertionError: Si el padre no es una instancia de tk.Tk o False.
            AssertionError: Si el ancho es menor o igual a 0.
            AssertionError: Si el alto es menor o igual a 0.
        """
        assert type(titulo) == str, "El título debe ser un string."
        assert type(ancho) == int, "El ancho debe ser un entero."
        assert type(alto) == int, "El alto debe ser un entero."
        assert (
            type(padre) in [tk.Tk, TkinterDnD.Tk] or padre == False
        ), "El padre debe ser una instancia de tk.Tk o False."
        assert type(DnD) == bool, "DnD debe ser un booleano."
        assert ancho >= 0, "El ancho debe ser mayor a 0."
        assert alto >= 0, "El alto debe ser mayor a 0."

        if not DnD:
            if padre == False:
                self.root = tk.Tk()
                self.root.config(bg=bg["window"])
                self.root.title(titulo)
                if not (ancho == 0 and alto == 0):
                    self.root.geometry(f"{ancho}x{alto}")
                self.mainFrame = tk.Frame(
                    self.root, bd=10, relief=tk.GROOVE, bg=bg["window"]
                )
                self.mainFrame.pack()
            else:
                self.root = tk.Toplevel(padre)
                self.root.config(bg=bg["window"])
                self.root.title(titulo)
                if not (ancho == 0 and alto == 0):
                    self.root.geometry(f"{ancho}x{alto}")
                self.mainFrame = tk.Frame(
                    self.root, bd=10, relief=tk.GROOVE, bg=bg["window"]
                )
                self.mainFrame.pack()
        else:
            if padre == False:
                self.root = TkinterDnD.Tk()
                self.root.config(bg=bg["window"])
                self.root.title(titulo)
                if not (ancho == 0 and alto == 0):
                    self.root.geometry(f"{ancho}x{alto}")
                self.mainFrame = tk.Frame(
                    self.root, bd=10, relief=tk.GROOVE, bg=bg["window"]
                )
                self.mainFrame.pack()
            else:
                self.root = tk.Toplevel(padre)
                self.root.config(bg=bg["window"])
                self.root.title(titulo)
                if not (ancho == 0 and alto == 0):
                    self.root.geometry(f"{ancho}x{alto}")
                self.mainFrame = tk.Frame(
                    self.root, bd=10, relief=tk.GROOVE, bg=bg["window"]
                )
                self.mainFrame.pack()

    def destroy(self) -> None:
        """
        Cierra la ventana.

        Returns:
            None
        """
        self.root.destroy()

    def mainloop(self) -> None:
        """
        Inicia el bucle principal de la ventana.

        Returns:
            None
        """
        self.root.mainloop()

    def config(self, **kwargs) -> None:
        """
        Configura la ventana.

        Args:
            **kwargs: Argumentos a configurar.

        Returns:
            None
        """
        self.root.config(**kwargs)
