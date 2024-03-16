destination = (
    r"C:\Users\spinc\Desktop\OCHO_FUEGOS\Datos del programa\NO TOCAR\costo_seco.pkl"
)
source = r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\costo_seco.xlsx"

import pandas as pd

df = pd.read_excel(source, dtype=str)
df.to_pickle(destination)
