destination = (
    r"C:\Users\spinc\Desktop\OCHO_FUEGOS\Datos del programa\NO TOCAR\flete_real.pkl"
)
source = r"C:\Users\spinc\Desktop\OCHO_FUEGOS\Datos del programa\NO TOCAR\flete_real.xlsx"

import pandas as pd

df = pd.read_excel(source, dtype=str)
df.to_pickle(destination)
