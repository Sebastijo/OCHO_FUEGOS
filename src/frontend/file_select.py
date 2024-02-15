"""
Este modulo tiene como objetivo crear un widget que permite al usuario seleccionar un archivo de Excel mediante drag and drop o mediante el botón "Examinar...".
El objeto toma como input el contenedor donde se creará el widget y el tipo de documento que se debe subir.
Empresa: Ocho Fuegos
Autor: Sebastián P. Pincheira
Fecha: 05/01/2024
Lenguaje: Python 3.11.7
Librerías:
- tkinter: 8.6.12
- tkinterdnd2: 0.2.1
"""

# Importamos paquetes
from typing import Union
import tkinter as tk
from tkinterdnd2 import *

# modulos propios
if __name__ == "__main__":
    import src.config.variables as var
else:
    from ..config import variables as var

# Variables universales:
background = var.bg["window"]


class BarraBusqueda:
    def __init__(
        self, contenedor: Union[tk.Frame, TkinterDnD.Tk], content: str
    ) -> None:
        """
        Inicializa una instancia de la clase BarraBusqueda.

        Args:
            contenedor (tk.Frame or TkinterDnD.Tk): Frame o ventana donde se creará el widget.
            content (str): Mensaje que se despliega en la barra de búsqueda.

        Returns:
            None
        """
        # Guardar el tipo de documento
        self.content = content

        # Crear el frame principal que contendrá todo el widget
        self.frame = tk.Frame(contenedor, bd=4, bg=background)

        # BARRA DE TEXTO:
        self.draggerFrame = tk.Frame(
            self.frame, bd=6, relief=tk.GROOVE, bg=background
        )  # Frame que contiene el widget de texto. Solo para motivos estéticos
        self.draggerFrame.grid(row=0, column=0)  # Ubicación del frame

        # Crear el widget de texto para mensajes y drag-and-drop
        self.dragger = tk.Text(
            self.draggerFrame,
            height=1,
            width=53,
            font=40,
            bg="#000000",  # Fondo negro
            fg="#FFFFFF",  # Texto blanco
            highlightthickness=1,
            insertbackground="#FFFFFF",  # Cursor de inserción blanco
        )
        self.dragger.insert("1.0", f"{self.content}")  # Texto inicial del widget

        # Binds
        self.dragger.bind(
            "<FocusIn>", lambda event: default_dragger(event, self.content)
        )  # Reemplazar el texto predeterminado al entrar
        self.dragger.bind(
            "<FocusOut>", lambda event: default_dragger(event, self.content)
        )  # Reemplazar el texto predeterminado al salir

        # Habilitar la funcionalidad de drag and drop
        self.dragger.drop_target_register(
            DND_ALL
        )  # Registrar el widget de texto como destino de drag and drop para todos los tipos de datos
        self.dragger.dnd_bind(
            "<<Drop>>", get_path
        )  # Asociar la función get_path al evento de soltar (Drop)

        self.dragger.pack()

        # BOTÓN DE EXAMINAR:
        self.button = tk.Button(
            self.frame,
            text="Examinar...",
            font=40,
            command=lambda: browsefunc(self.dragger),
            bd=4,
            bg="#7A7A7A",  # Fondo gris
            activebackground="#DDDDDD",  # Fondo al pasar el mouse
            cursor="based_arrow_up",
        )
        self.button.bind("<Enter>", on_enter_examinar)
        self.button.bind("<Leave>", on_leave_examinar)

        self.button.grid(row=0, column=1)

    def pack(self):
        """Método para empaquetar el widget en el contenedor."""
        self.frame.pack()

    def grid(self, *args, **kwargs):
        """Método para empaquetar el widget en el contenedor."""
        self.frame.grid(*args, **kwargs)

    def place(self, *args, **kwargs):
        """Método para empaquetar el widget en el contenedor."""
        self.frame.place(*args, **kwargs)

    def get(self, *args, **kwargs) -> str:
        """Método para obtener texto del widget de texto."""
        return self.dragger.get(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Método para eliminar texto del widget de texto."""
        self.dragger.delete(*args, **kwargs)

    def insert(self, *args, **kwargs):
        """Método para insertar texto en el widget de texto."""
        self.dragger.insert(*args, **kwargs)


# Función que se llama cuando se realiza un evento de arrastrar y soltar (drag and drop)
def get_path(event):
    text = event.data
    event.widget.delete(1.0, tk.END)
    event.widget.insert(tk.END, text)


# Función para manejar el comportamiento predeterminado al enfocar el cuadro de entrada
def default_dragger(event, content):
    current = event.widget.get("1.0", tk.END)
    if current == content + "\n":
        event.widget.delete("1.0", tk.END)
    elif current == "\n":
        event.widget.insert(tk.END, content)


# Animaciones de buton "Examinar..."
def on_enter_examinar(event):
    event.widget["background"] = "#DDDDDD"


def on_leave_examinar(event):
    event.widget["background"] = "#7A7A7A"


def browsefunc(text: tk.Widget) -> None:
    file_types = [
        ("All Files", "*.*"),
        ("Excel Files", "*.xlsx;*.xls"),
        ("PDF Files", "*.pdf"),
    ]
    filename = tk.filedialog.askopenfilename(filetypes=file_types)
    text.delete("1.0", tk.END)
    text.insert(tk.END, filename)


# Probamos la clase BarraBusqueda
if __name__ == "__main__":
    from src.frontend.ventana import Ventana

    ventana_test = Ventana("Test", DnD=True)
    mainFrame_test = ventana_test.mainFrame
    barra1 = BarraBusqueda(mainFrame_test, "Seleccione un archivo .xls de embarques")
    barra2 = BarraBusqueda(mainFrame_test, "Seleccione un archivo .xls de facturas")
    barra1.pack()
    barra2.pack()
    ventana_test.mainloop()
