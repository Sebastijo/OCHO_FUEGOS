"""
Archivo con las variables universales. La idea es llamar desde acá a todas las variables que se necesiten en distintos archivos del programa.
"""

import os
import sys
import re
import platform
from pathlib import Path

app_name : str = "Ocho Fuegos-Cherry Manager"

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

    assert isinstance(app_name, str), f"app_name must be a string, not {type(app_name_strin)}"
    
    app_name = re.sub(r'\W', '_', app_name)

    os_type = platform.system()
    
    if os_type == 'Windows':
        support_dir = Path(os.getenv('APPDATA')) / app_name
    elif os_type == 'Darwin':  # macOS
        support_dir = Path(os.path.expanduser('~')) / 'Library' / 'Application Support' / app_name
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
