"""
El objetivo de este modulo es agregar datos al control de pagos.
Se crea uan función que recibe los datos correspondientes a un fila de control de pagos
y los agrega a la base de datos. La inteción inicial es que esta función sea usada para
agregar datos a la base de datos desde la interfaz gráfica.
"""

# Importamos las librerias necesarias
import pandas as pd
from datetime import datetime

# Leemos el control de pagos guardado en el cache 
# (por ahora el cache no existe, remplazar lo que viene a continuación)
control_de_pagos_dict = {
        "Cliente": [],
        "Fecha Pago": [],
        "País Destino": [],
        "Ingreso": [],
        "Observación": [],
    }
control_de_pagos = pd.DataFrame(control_de_pagos_dict)

def agregar_pago(cliente: str, fecha: datetime, pais: str, ingreso: float, observacion: str) -> None:
    """
    Agrega un pago al control de pagos.

    Args:

    """
    control_de_pagos = control_de_pagos.append({
        "Cliente": cliente,
        "Fecha Pago": fecha,
        "País Destino": pais,
        "Ingreso": ingreso,
        "Observación": observacion,
    }, ignore_index=True)


# Guadramos el DataFrame en algún formato en alguna carpeta:
#...