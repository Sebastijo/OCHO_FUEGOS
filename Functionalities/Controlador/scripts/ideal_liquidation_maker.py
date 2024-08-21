from Functionalities.Controlador.src.backend.interpreters.BQ_interpreter import interpreter_BQ

objective_dir = r"C:\Users\spinc\OneDrive\Escritorio\ideal_format"

example1 = r"C:\Users\spinc\OneDrive\Documentos\Coding\OCHO_FUEGOS\Functionalities\Controlador\data\input\Liquidaciones\BQ_Sales Report-8F-AIR-045-91458345-X.xlsx"

output, _ = interpreter_BQ(example1)

output = output[0]

# Turn every element from the list `output` into a different page of an excel file

import pandas as pd

with pd.ExcelWriter(objective_dir + "\\output.xlsx") as writer:
    for i, page in enumerate(output):
        pd.DataFrame(page).to_excel(writer, sheet_name=f"Page {i+1}", index=False)
