"""
El objetivo de este modulo es pasar los resultados del programa a un formato legible y util para el usuario.
Autor: Sebastián P. Pincheira
Fecha: 6/03/2024
Lenguaje: Python 3.11.7
Librerías:
- pandas: 2.2.0
"""

# importamos librerias necesarias
import os
import pandas as pd

# importamos modulos propios
if __name__ == "__main__":
    from src.config import variables as var
else:
    from ..config import variables as var

directory = var.directory
datos_folder = os.path.join(directory, "Datos del programa")
control_path = os.path.join(datos_folder, "output", "Control.xlsx")

if __name__ == "__main__":
    control_pickle = (
        r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\pickles\controlFinal.pkl"
    )
    liq_no_pareadas_pickle = (
        r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\pickles\liq_no_pareadas.pkl"
    )
    no_vendidos_pickle = (
        r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\pickles\no_vendidos.pkl"
    )
    if not (
        os.path.exists(control_pickle)
        and os.path.exists(liq_no_pareadas_pickle)
        and os.path.exists(no_vendidos_pickle)
    ):
        from src.backend.control_final import control

        embarque_path = (
            r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\Base embarques.xlsx"
        )
        facturas_path = (
            r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\Facturas proformas.xlsx"
        )
        tarifas_path = r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\Tarifas.xlsx"
        liquidaciones_path = (
            r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\Liquidaciones"
        )

        os.remove(control_pickle) if os.path.exists(control_pickle) else None
        (
            os.remove(liq_no_pareadas_pickle)
            if os.path.exists(liq_no_pareadas_pickle)
            else None
        )
        os.remove(no_vendidos_pickle) if os.path.exists(no_vendidos_pickle) else None
        control_df, errores, revisar, liquidaciones_no_pareadas, no_vendidos = control(
            embarque_path, facturas_path, tarifas_path, liquidaciones_path
        )

        control_df.to_pickle(control_pickle)
        liquidaciones_no_pareadas.to_pickle(liq_no_pareadas_pickle)
        no_vendidos.to_pickle(no_vendidos_pickle)

    control_df = pd.read_pickle(control_pickle)
    liquidaciones_no_pareadas = pd.read_pickle(liq_no_pareadas_pickle)
    no_vendidos = pd.read_pickle(no_vendidos_pickle)


def export(
    control_df: pd.DataFrame, liq_no_pareadas: pd.DataFrame, no_vendidos: pd.DataFrame
):
    """
    Esta función toma los resultados del programa y los exporta a un archivo Excel.

    Args:
        control_df (pd.DataFrame): DataFrame con los resultados del programa.
        liq_no_pareadas (pd.DataFrame): DataFrame con las liquidaciones no pareadas.
        no_vendidos (pd.DataFrame): DataFrame con los productos no vendidos.

    Returns:
        None

    Raises:
        AssertionError: Si control_df, liq_no_pareadas o no_vendidos no son DataFrames de pandas.
    """

    assert isinstance(
        control_df, pd.DataFrame
    ), "control_df debe ser un DataFrame de pandas."
    assert isinstance(
        liq_no_pareadas, pd.DataFrame
    ), "liq_no_pareadas debe ser un DataFrame de pandas."
    assert isinstance(
        no_vendidos, pd.DataFrame
    ), "no_vendidos debe ser un DataFrame de pandas."

    # Function to apply formatting to a sheet
    def apply_formatting(worksheet, df):
        header_format = workbook.add_format(
            {"bold": True, "fg_color": "#6FAAFF", "border": 1}
        )
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)

            column_len = df[value].astype(str).str.len().max()
            column_len = max(column_len, len(value)) + 3
            worksheet.set_column(col_num, col_num, column_len)

    # Creamos el Excel de output
    with pd.ExcelWriter(control_path, engine="xlsxwriter") as writer:
        # Convert the original dataframe (control_df) to an XlsxWriter Excel object
        control_df.to_excel(
            writer, sheet_name="Control", startrow=1, header=False, index=False
        )

        workbook = writer.book
        worksheet1 = writer.sheets["Control"]

        # Apply formatting to Control
        apply_formatting(worksheet1, control_df)

        # Add Liquidaciones no pareadas with liq_no_pareadas
        liq_no_pareadas.to_excel(
            writer,
            sheet_name="Liquidaciones no pareadas",
            startrow=1,
            header=False,
            index=False,
        )
        worksheet2 = writer.sheets["Liquidaciones no pareadas"]

        # Apply formatting to Liquidaciones no pareadas
        apply_formatting(worksheet2, liq_no_pareadas)

        # Add No vendidos with no_vendidos
        no_vendidos.to_excel(
            writer, sheet_name="No vendidos", startrow=1, header=False, index=False
        )
        worksheet3 = writer.sheets["No vendidos"]

        # Apply formatting to No vendidos
        apply_formatting(worksheet3, no_vendidos)


if __name__ == "__main__":
    export(control_df, liquidaciones_no_pareadas, no_vendidos)
    print(f"El archivo {control_path} ha sido creado con éxito.")
