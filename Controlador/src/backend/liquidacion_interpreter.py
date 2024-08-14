"""
El objetivo de este módulo es intepretar los distintos tipos de liquidaciones que se pueden realizar en el sistema.
Los tipos de liquidaciones disponibles son:

    - 12Islands (.pdf)
    - JumboFruit (.xlsx)
    - 8F (.xlsx)
    - Happy Farm Fruit (.xlsx)

El resultado de el módulo es producir una lista de listas, cada lista representando un embarque y los elementos de la lista representadno los diversos datos presentes en un embarque.
Cada formato tendrá su función que lo traduce. Los formatos se relacionan de la siguiente manera.

-
-Happy Farm Fruit (HFF) es traducido al formato standard 8F.
-Jumbo Fruit (BQ) es traducido al formmato standard 8F.
-El formato standard 8F es traducido al formato 12Islands.

Empresa: Ocho Fuegos
Autor: Sebastián P. Pincheira
Fecha: 10/01/2024
Lenguaje: Python 3.11.7
Librerías:
- pandas: 2.2.0
- numpy: 1.24.2
- sympy: 1.12
- tabula: 2.9.0
"""

# Importación de librerías
import pandas as pd
import numpy as np

# import tabula
import os

# importamos modulos porpios
if __name__ == "__main__":
    from src.config import variables as var
    from src.backend.interpreters.HT_interpreter import interpreter_12Islands
    from src.backend.interpreters.HFF_interpreter import interpreter_HFF
    from src.backend.interpreters.HFF_SEA_interpreter import interpreter_HFF_SEA
    from src.backend.interpreters.BQ_interpreter import interpreter_BQ
    from src.backend.interpreters.standard_interpreter import interpreter_standard
else:
    from ..config import variables as var
    from .interpreters.HT_interpreter import interpreter_12Islands
    from .interpreters.HFF_interpreter import interpreter_HFF
    from .interpreters.HFF_SEA_interpreter import interpreter_HFF_SEA
    from .interpreters.BQ_interpreter import interpreter_BQ
    from .interpreters.standard_interpreter import interpreter_standard

# Definimos variables globales
main_dict_liq_standard = var.main_dict_liq_standard
main_dict_liq_JF = var.main_dict_liq_JF
main_list_liq_HFF = var.main_list_liq_HFF
main_list_liq_HFF_SEA = var.main_list_liq_HFF_SEA

if __name__ == "__main__":
    example1 = r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\Liquidaciones\BQ_Sales Report-8F-AIR-045-91458345-X.xlsx"
    example2 = r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\Liquidaciones\BQ_Sales Report-8F-BY SEA-FSCU5743414.xlsx"


def interpreter(liquidacion: str) -> tuple[list, list]:
    """
    Esta función interpreta los datos de un archivo de liquidación y devuelve una tupla con las siguientes coordenadas:

    0) Lista de listas con la informacion de la liquidación.
    1) Lista de enteros con las páginas de la liquidación.

    Args:
        liquidacion (str): Ruta del archivo de liquidación.

    Returns:
        list: Lista de listas con los datos de la liquidación.

    Raises:
        AssertionError: Si el archivo de liquidación no existe, no es un archivo o no es un archivo .pdf o .xlsx.
    """
    assert os.path.exists(liquidacion), f"El archivo '{liquidacion}' no existe."
    assert os.path.isfile(liquidacion), f"El archivo '{liquidacion}' no es un archivo."
    assert liquidacion.endswith(
        (".pdf", ".xlsx", ".xls")
    ), f"El archivo '{liquidacion}' no es un archivo .pdf o .xlsx."

    filename = filename = os.path.basename(liquidacion)

    assert (
        filename.startswith("HT")
        or filename.startswith("8F")
        or filename.startswith("HFF")
        or filename.startswith("BQ")
    ), f"No se pudo detectar el formato del archivo {filename}, asegurece que empiece con alguno de los siguientes: 'HT', '8F', 'HFF', 'BQ'."

    # Verificamos el tipo de liquidación
    if filename.startswith("HT"):
        liquidacion_list = interpreter_12Islands(liquidacion)
    elif filename.startswith("8F"):
        liquidacion_list = interpreter_standard(liquidacion)
    elif filename.startswith("BQ"):
        liquidacion_list = interpreter_BQ(liquidacion)
    elif filename.startswith("HFF"):
        if filename[4:].startswith("SEA"):
            liquidacion = interpreter_HFF_SEA(liquidacion)
        liquidacion_list = interpreter_HFF(liquidacion)

    return liquidacion_list


if __name__ == "__main__":
    embarque_example1, page_example1 = interpreter(example1)
    print("Example1:")
    print("Main:")
    print(embarque_example1[0][0])
    print("Cost:")
    print(embarque_example1[0][1])
    print("Note:")
    print(embarque_example1[0][2])
    print()

    embarque_example2, page_example2 = interpreter(example2)
    print("Example2:")
    print("Main:")
    print(embarque_example2[0][0])
    print("Cost:")
    print(embarque_example2[0][1])
    print("Note:")
    print(embarque_example2[0][2])
    print()
