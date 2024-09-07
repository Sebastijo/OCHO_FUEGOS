"""
El objetivo de este modulo es calcular el saldo de cada cliente en base a la información
control de pagos y boleta.
"""

import pandas as pd

from src.config.universal_variables import pagos_dir
from .control_de_pagos import control_de_pagos_path
from .boleta import boleta_path

def actualizar_moneyLabel(widget: MoneyLabel) -> None:
    """
    Actualiza el valor de un `MoneyLabel` a partir de `control_de_pago`.
    """
    cliente = widget.cliente
    money = control_de_pagos[control_de_pagos["Cliente"] == cliente]["Ingreso"].sum()
    widget.set_value(money)

def actualizar_moneyLabels(moneyLabels: list[MoneyLabel]) -> None:
    """
    Actualiza el valor de una lista de `MoneyLabel` a partir de `control_de_pago`.
    """
    for widget in moneyLabels:
        actualizar_moneyLabel(widget)