import pandas as pd

embarque_path = r"C:\Users\spinc\OneDrive\Documentos\Coding\OCHO_FUEGOS\Functionalities\Pagos\data\testing_data\Base embarques.xlsx"

embarque_df = pd.read_excel(embarque_path)

potential_keys = embarque_df.columns[(embarque_df.nunique() == len(embarque_df)) & (embarque_df.isnull().sum() == 0)]

print("Embarques key:")
print(list(potential_keys))


# de esto se concluye que "PalletRowId" es la llave primaria de la tabla de embarques

contrato_path = r"C:\Users\spinc\OneDrive\Documentos\Coding\OCHO_FUEGOS\Functionalities\Pagos\data\testing_data\Precios Contrato Programa Pagos.xlsx"

contrato_df = pd.read_excel(contrato_path)

columns_to_check = ["Cliente", "Calibre", "KG Caja"]

unique_rows = contrato_df[columns_to_check].drop_duplicates()
is_unique = len(unique_rows) == len(contrato_df)

all_non_null = contrato_df[columns_to_check].notna().all().all()

print(columns_to_check, " are unique and all non-null in contrato contrato_df:")
print(is_unique, all_non_null)

print(contrato_df["Cliente"].unique())

print(embarque_df["ReceiverName"].unique())