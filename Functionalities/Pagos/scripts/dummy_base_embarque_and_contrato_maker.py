import pandas as pd
from pathlib import Path

data_dit = Path(r"C:\Users\spinc\OneDrive\Documentos\Coding\OCHO_FUEGOS\data")

embarques_path = data_dit / "dummy_base_embarques.xlsx"
contratos_path = data_dit / "dummy_contratos.xlsx"

embarques_columns = ["PalletRowId", "ReceiverName", "CaliberName", "PackageNetWeight"]
contratos_columns = ["Cliente", "Calibre", "KG Caja", "Precio"]

embarques = pd.DataFrame(
    {
        "PalletRowId": [1, 2, 3, 4, 5],
        "ReceiverName": ["Cliente1", "Cliente2", "Cliente3", "Cliente1", "Cliente2"],
        "CaliberName": ["XL", "XLD", "XLDD", "XLD", "XL"],
        "PackageNetWeight": [2.5, 2.5, 5.0, 5.0, 10.0],
        "Quantity": [100, 200, 300, 50, 100],
    }
)

contratos = pd.DataFrame(
    {
        "Cliente": ["Cliente1", "Cliente2", "Cliente3", "Cliente1", "Cliente2"],
        "Calibre": ["XL", "XLD", "XLDD", "XLD", "XL"],
        "KG Caja": [2.5, 2.5, 5.0, 5.0, 10.0],
        "Precio": [10, 20, 30, 50, 60],
    }
)

embarques.to_excel(embarques_path, index=False)
contratos.to_excel(contratos_path, index=False)
