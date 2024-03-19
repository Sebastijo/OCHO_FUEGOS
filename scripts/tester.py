import pandas as pd
import json
import os

# Replace 'your_excel_file.xlsx' with the actual path to your Excel file
excel_file_path = r"C:\Users\spinc\Desktop\OCHO_FUEGOS\precios contrato programa.xlsx"

# Read the Excel file into a pandas DataFrame
df = pd.read_excel(excel_file_path)

# Replace 'output_pickle_file.pkl' with the desired name for your pickle file
pickle_file_path = r"C:\Users\spinc\Desktop\OCHO_FUEGOS\src\config\precios_contrato.pkl"

# Save the DataFrame to a pickle file
if not os.path.exists(pickle_file_path):
    df.to_pickle(pickle_file_path)

COD_PUERTO_DESTINO = {
    "SHANGHAI AIRPORT": "411",
    "GUANGZHOU AIRPORT": "411",
    "CHANGSHA - HUANGHUA": "411",
    "HONG KONG": "301",
    "SHANGHAI": "301",
    "SHENZHEN": "411",
    "XIAMEN": "411",
    "ZHENGZHOU AIRPORT": "411",
    "BANGKOK": "319",
    "MADRID": "517",
    "MANILA": "335",
    "SAO PAULO": "291",
    "SAO PAULO AIRPORT": "220",
    "SINGAPUR": "332",
}

if not os.path.exists(
    os.path.join(
        r"C:\Users\spinc\Desktop\OCHO_FUEGOS\src\config", "cod_puerto_destino.json"
    )
):
    with open(
        os.path.join(
            r"C:\Users\spinc\Desktop\OCHO_FUEGOS\src\config", "cod_puerto_destino.json"
        ),
        "w",
    ) as file:
        json.dump(COD_PUERTO_DESTINO, file)
