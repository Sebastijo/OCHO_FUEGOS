"""
El objetivo de este modulo es calcular el saldo de cada cliente en base a la información
control de pagos y boleta.
"""

from pathlib import Path
import pandas as pd

from src.config.universal_variables import pagos_dir
from .control_de_pagos import control_de_pagos_path
from .boleta import boleta_path
from ..frontend.moneyLabel import MoneyLabel



def actualizar_moneyLabels(moneyLabels: list[MoneyLabel]) -> None:
    """
    Actualiza el valor de una lista de `MoneyLabel` a partir de `control_de_pago` y una boleta.
    """

    control_de_pagos = pd.read_csv(
        control_de_pagos_path, usecols=["Cliente", "Ingreso"]
    )
    boleta = pd.read_csv(boleta_path, usecols=["Cliente", "Precio"])

    for widget in moneyLabels:
        client = widget.cliente
        if client not in control_de_pagos["Cliente"].values:
            data = {
                "Cliente": [client],
                "Ingreso": [0],
            }
            control_de_pagos = pd.concat(
                [control_de_pagos, pd.DataFrame(data)], ignore_index=True
            )

        if client not in boleta["Cliente"].values:
            data = {
                "Cliente": [client],
                "Precio": [0],
            }
            boleta = pd.concat([boleta, pd.DataFrame(data)], ignore_index=True)

    if len(moneyLabels) == 1:
        widget = moneyLabels[0]
        pagos = control_de_pagos[control_de_pagos["Cliente"] == widget.cliente].sum()
        boletas = boleta[boleta["Cliente"] == widget.cliente].sum()
        money = pagos["Ingreso"] - boletas["Precio"]
        widget.set_value(money)
    else:
        grouped_control_de_pagos = control_de_pagos.groupby("Cliente").sum()
        grouped_boleta = boleta.groupby("Cliente").sum()

        money = grouped_control_de_pagos["Ingreso"] - grouped_boleta["Precio"]

        for widget in moneyLabels:
            widget.set_value(money[widget.cliente])
