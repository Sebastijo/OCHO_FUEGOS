"""
Interface de usuario gráfica para el programa de automatisación de procesos corporativos, sección de ventas.
El objetivo del siguiente programa es crear una GUI a partir de tkinter para el programa de automatisación de procesos corporativos.
Empresa: Ocho Fuegos
Autor: Sebastián P. Pincheira
Fecha: 03/01/2024
Lenguaje: Python 3.11.7
Librerías:
- tkinter: 8.6.12
- tkinterdnd2: 0.2.1
- pandas: 2.2.0
"""

# Importación de bibliotecas necesarias
import tkinter as tk
from tkinterdnd2 import *
import pandas as pd
from xlsxwriter.workbook import Workbook
import os

# modulos propios
if __name__ == "__main__":
    from src.frontend.file_select import BarraBusqueda
    from src.frontend.buttons import Boton
    import src.config.variables as var
    from src.frontend.info_window import InfoBoton
    from src.frontend.error_window import inputErrorWindow, revisarWindow
    from src.backend.control_final import control
    from src.frontend.ventana import Ventana
else:
    from .file_select import BarraBusqueda
    from .buttons import Boton
    from ..config import variables as var
    from .info_window import InfoBoton
    from .error_window import inputErrorWindow, revisarWindow
    from ..backend.control_final import control
    from .ventana import Ventana


# Variables universales:
bg = var.bg  # Color de fondo
fg = var.fg  # Color de texto
title = var.title  # Título de la ventana principal

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


# Acción del botón de ejecución
def runVentas() -> dict:
    """
    Función que se ejecuta al presionar el botón de ejecución.
    """
    # Guardamos los paths de los archivos seleccionados
    inputPaths = {}  # Diccionario que contiene los paths de los archivos seleccionados
    for tipo in barrasBusqueda:
        inputPaths[tipo] = barrasBusqueda[tipo].get("1.0", "end-1c").replace("/", "\\")

    # Ejecutamos el programa de ventas
    control_df, errores, revisar = control(
        inputPaths["embarques"],
        inputPaths["facturas"],
        inputPaths["tarifas"],
        inputPaths["liquidaciones"],
    )

    # Ubicación deonde se guarde el control de embarques
    control_path = (
        r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\output\program_output\control.xlsx"
    )

    if not inputErrorWindow(
        root
    ):  # Verificamos error y, a la vez, mostramos errorWindow en caso de haber.
        frameFinalButtons.grid_forget()  # Borramos los botones finales

        # Creamos el Excel de output
        if os.path.exists(control_path):  # Si el archivo existe, lo borramos
            os.remove(control_path)
        writer = pd.ExcelWriter(control_path, engine="xlsxwriter")

        # Convert the dataframe to an XlsxWriter Excel object. Note that we turn off
        # the default header and skip one row to allow us to insert a user defined
        # header. Also remove index values by index=False
        control_df.to_excel(
            writer, sheet_name="Sheet1", startrow=1, header=False, index=False
        )

        workbook = writer.book
        worksheet = writer.sheets["Sheet1"]
        # Add a header format.
        header_format = workbook.add_format(
            {"bold": True, "fg_color": "#6FAAFF", "border": 1}
        )
        for col_num, value in enumerate(control_df.columns.values):
            worksheet.write(0, col_num, value, header_format)

            column_len = control_df[value].astype(str).str.len().max()
            # Setting the length if the column header is larger
            # than the max column value length
            column_len = max(column_len, len(value)) + 3
            # set the column length
            worksheet.set_column(col_num, col_num, column_len)

        # Close the Pandas Excel writer and output the Excel file.
        writer.close()
        # Cambiamos el texto de los outputs
        output[0].configure(
            text=f"El resultado se encuentra disponible en\r {control_path}"
        )
        num_errores = sum(len(definition) for definition in errores.values())
        num_revisar = len(revisar)
        if num_errores + num_revisar == 0:
            output[1].configure(text="No se detectaron errores en la ejecución")
        else:
            output[1].configure(
                text=f"Hubo {num_errores} embarques cuya liquidación no se pudo leer\r y {num_revisar} embarques cuyas liquidaciones tienen inconsistencias"
            )
            output[-1].pack(padx=10, pady=(10, 10))
            output[-1].configure(command=lambda: revisarWindow(root, errores, revisar))
        outputFrame.grid(row=1, column=0)  # Mostramos el frame de los outputs
        frameFinalButtons.grid(
            row=2, column=0, sticky=tk.E
        )  # Mostramos los botones finales
        return
    else:  # Se detectan errores
        return


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

# Creación de los botones finales de output y de exit.
frameFinalButtons = tk.Frame(mainFrame, bd=4, bg=bg["window"])
info = InfoBoton(
    frameFinalButtons,
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean euismod bibendum laoreet."
    + " Proin gravida dolor sit amet lacus accumsan et viverra justo commodo."
    + " Proin sodales pulvinar tempor. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus."
    + " Nam fermentum, nulla luctus pharetra vulputate,"
    + " Felis tellus mollis orci, sed rhoncus sapien nunc eget odio. Lorem ipsum dolor sit amet, consectetur adipiscing elit."
    + " Aenean euismod bibendum laoreet. Proin gravida.",
)  # Boton de información sobre el programa
ejecutar = Boton(
    frameFinalButtons, "Ejecutar", lambda: print("Ejecutar"), "output_button"
)  # Botón de ejecución
salir = Boton(frameFinalButtons, "Salir", root.quit, "exit_button")  # Botón de salida


# Definimos el command del boton ejecutar
ejecutar.configure(command=runVentas)

# Cargamos los botones a la ventana
frameFinalButtons.grid(row=1, column=0, sticky=tk.E)

info.pack(side=tk.LEFT, anchor="n")
salir.pack(side=tk.RIGHT, anchor="n")
ejecutar.pack(side=tk.RIGHT, anchor="n")


# Inicio del bucle principal para la ejecución de la interfaz gráfica
root.mainloop()
