"""
Archivo con las variables universales. La idea es llamar desde acá a todas las variables que se necesiten en distintos archivos del programa.
"""

import os
import sys
import re
import platform
from pathlib import Path
import time

app_name: str = "Ocho Fuegos-Cherry Manager"

try:
    start_time
except NameError:
    start_time = time.time()


def get_support_dir(app_name: str) -> Path:
    """
    Returns the directory where the application should store its data
    (Usually in APPDATA on Windows and in Application Support on macOS).

    Args:
        app_name (str): The name of the application.

    Returns:
        Path: The directory where the application should store its data.

    Raises:
        AssertionError: If app_name is not a string.
        OSError: If the operating system is not supported.
    """

    assert isinstance(
        app_name, str
    ), f"app_name must be a string, not {type(app_name_strin)}"

    app_name = re.sub(r"\W", "_", app_name)

    os_type = platform.system()

    if os_type == "Windows":
        support_dir = Path(os.getenv("APPDATA")) / app_name
    elif os_type == "Darwin":  # macOS
        support_dir = (
            Path(os.path.expanduser("~")) / "Library" / "Application Support" / app_name
        )
    else:
        raise OSError(f"Unsupported OS: {os_type}")

    support_dir.mkdir(parents=True, exist_ok=True)
    return support_dir


directory = get_support_dir(app_name)
print(directory)

controlador_dir = directory / "controlador"
controlador_output_dir = controlador_dir / "output"
controlador_variables_dir = controlador_dir / "Variables"
controlador_back_up_variables_dir = controlador_dir / "back_up_variables"
controlador_dir.mkdir(parents=True, exist_ok=True)
controlador_output_dir.mkdir(parents=True, exist_ok=True)
controlador_back_up_variables_dir.mkdir(parents=True, exist_ok=True)

pagos_dir = directory / "pagos"
pagos_dir.mkdir(parents=True, exist_ok=True)

embarque_path_pointer = pagos_dir / "ubicación_base_embarques.txt"
contratos_path_pointer = pagos_dir / "ubicación_base_contratos.txt"


def get_pointer_path(pointer_path: Path, pointer_name: str) -> Path:
    """
    Returns the path of a pointer file. A pointer file is a .txt file witgh just the path of a file that is being pointed to.

    Args:
        pointer_path (Path): The path of the pointer file.
        pointer_name (str): The name of the pointer file.

    Returns: path of the file that is being pointed to.
    """

    try:
        with open(pointer_path, "r") as f:
            path = Path(f.read().strip())
        try:  # HERE
            path_exists = path.exists()
        except:
            raise FileNotFoundError(f"File not found: {path}")
        if not path_exists:
            raise FileNotFoundError(f"File not found: {path}")
        if not path.is_file():
            raise FileNotFoundError(f"Pointer file should not point to a file: {path}")
        if not path.suffix in [".xlsx", ".xls", ".csv"]:
            raise FileNotFoundError(
                f"Pointer file should point to an Excel or CSV file: {path}"
            )
        return path

    except FileNotFoundError:
        with open(pointer_path, "w") as f:
            f.write(
                (
                    f"NO SE ENCONTRÓ LA UBICACIÓN DE LA {pointer_name}.\n"
                    "Remplace todo el contenido de este archivo con la ubicación de la "
                    f"{pointer_name} en su computadora y luego abra el programa nuevamente.\n"
                    "El formato del archivo debe ser Excel.\n"
                    f"Por ejemplo, si la ubicación de la {pointer_name} es "
                    '"C:/Users/Usuario/Documents/ejemplo.xlsx", entonces el contenido de este archivo '
                    "debería ser únicamente:\n\n"
                    "C:/Users/Usuario/Documents/ejemplo.xlsx\n"
                )
            )

        if platform.system() == "Windows":
            os.startfile(pointer_path)
            sys.exit()
        elif platform.system() == "Darwin":
            os.system(f'open "{pointer_path}"')
            sys.exit()
        else:
            os.system(f'xdg-open "{pointer_path}"')
            sys.exit()


stock_dir = directory / "stock"
stock_dir.mkdir(parents=True, exist_ok=True)

stock_limits_path_pointer = stock_dir / "ubicación_base_stock_limits.txt"
