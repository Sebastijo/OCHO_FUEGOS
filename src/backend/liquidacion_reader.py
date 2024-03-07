"""
El objetivo de este modulo es tomar una carpeta de liquidación y extraer la información de las tablas de cada PDF
contenido en la carpeta para ser agregado a un archivo de control de liquidaciones.
Este modulo contiene todo el proceso de liquidaciones y no contine la información del resto del proceso de ventas.
Empresa: Ocho Fuegos
Autor: Sebastián P. Pincheira
Fecha: 10/01/2024
Lenguaje: Python 3.11.7
Librerías:
- pandas: 2.2.0
- numpy: 1.24.2
- tabula: 2.9.0
"""

# Importamos paquetes
import os
import pandas as pd
import numpy as np


# Moduos propios
if __name__ == "__main__":
    from src.config import variables as var
    from src.backend.embarque_liquidacion_class import embarqueL
    from src.backend.liquidacion_revisar import revisar_liquidacion
    from src.backend.liquidacion_interpreter import interpreter
else:
    from ..config import variables as var
    from .embarque_liquidacion_class import embarqueL
    from .liquidacion_revisar import revisar_liquidacion
    from .liquidacion_interpreter import interpreter

# Importamos variables globales
main_dict_liq = var.main_dict_liq
key_liq = var.key_liq
key_liq_incompleto = var.key_liq_incompleto

if __name__ == "__main__":
    # Path to the liquidaciones folder
    folder = r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\Liquidaciones"

    # Ejemplos de liquidaciones reales
    liquidacion = r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\Liquidaciones\BQ_Sales Report-8F-BY SEA-FSCU5743414.xlsx"
    liquidacion_triple = r"C:\Users\spinc\Desktop\OCHO_FUEGOS\data\input\Liquidaciones\tester_3_hojas.pdf"


# The following is called "embarques_three_tables" since, before update, it took a list of lists of DataFrames and returned
# a list of lists of DataFrames with only three (3) DataFrames corresponding to the main, cost, and note tables.
def embarques_three_tables(
    embarques: list[list], paginas: list[int]
) -> tuple[list, list, list]:
    """
    Takes a list of lists of DataFrames and returns, on the first coordinate, a list of dictonaries with the words "main", "cost", "note", "main_summary"
    where the definition corresponds to the DataFrame associated to that category. This list excludes all errors found.
    On the second category, a list with the pages where errors where found is returned.


    Args:
        embarques (list): List of lists of DataFrames
        paginas (list): List of integers

    Returns:
        tuple: tuple with tres coordinates (list, list, list)

    Raises:
        AssertionError: If embarques is not a list
        AssertionError: If paginas is not a list
        AssertionError: If the length of embarques and paginas is not equal
        AssertionError: If the number of embarques is not the same as before
    """
    assert type(embarques) == list, "embarques no es una lista"
    assert type(paginas) == list, "paginas no es una lista"
    assert len(embarques) == len(
        paginas
    ), "La cantidad de embarques y páginas no es igual"

    def df_formatter(df: pd.DataFrame) -> pd.DataFrame:
        """
        Function that takes in a DataFrame and returns the same DataFrame with the following changes:
        - Remove Chinese characters from column names
        - Remove Chinese characters from DataFrame content
        - Remove leading slash in all columns
        - Remove leading spaces and replace leading slash in column names
        - Remove leading spaces in DataFrame content
        """
        # Remove nan rows
        df = df.dropna(how="all")
        # Remove Chinese characters from column names
        df.columns = df.columns.str.replace("[^\x00-\x7F]+", "", regex=True)
        # Remove Chinese characters from DataFrame content
        # df = df.applymap(lambda x: "".join(filter(lambda char: char.isascii(), str(x)))) // depricated
        df = df.apply(
            lambda x: x.map(
                lambda char: "".join(filter(lambda c: c.isascii(), str(char)))
            )
        )
        # Remove leading slash in all columns
        # df = df.applymap(lambda x: x.lstrip("/$") if isinstance(x, str) else x) // depricated
        df = df.apply(
            lambda x: x.map(
                lambda element: (
                    element.lstrip("/$") if isinstance(element, str) else element
                )
            )
        )
        # Remove leading spaces and replace leading slash in column names
        df.columns = df.columns.str.strip().str.replace("^/", "", regex=True)
        # Remove leading spaces in DataFrame content
        df = df.apply(
            lambda x: x.map(
                lambda element: element.strip() if isinstance(element, str) else element
            )
        )
        return df

    def add_df(df1: pd.DataFrame, df2: pd.DataFrame) -> tuple:
        """
        Función que agrega un data frame df2 a un otro data frame df1 tratando las columnas de df2 como una fila.
        Entrega True si todo es correcto, False si no (en la segunda coordenada).
        """
        if len(df1.columns) != len(df2.columns):
            return None, False
        # Agregamos las columnas de df2 como la primera fila de df2
        # DataFrame con las columnas de df2 como la única fila
        fake_header = pd.DataFrame(df2.columns).T
        fake_header.columns = (
            df1.columns
        )  # Cambiamos el nombre de las columnas para que coincidan con las de df1
        df2.columns = (
            df1.columns
        )  # Cambiamos el nombre de las columnas para que coincidan con las de df1
        df2 = pd.concat(
            [fake_header, df2]
        )  # Corresponde al df2 con sus columnas originales en la primera fila y su nuevo nombre de columnas correspondiendo al df1

        # Agregamos el df2 al df1
        df1 = pd.concat([df1, df2]).reset_index(drop=True)

        return df1, True

    # Agrupamos las tablas en las tres (3) categorías que existen
    embarques_ = []  # Corresponds to the new embarques with only three (3) tables
    paginas_ = []  # Corresponds to the first page of each embarque_ of embarques_
    errores = []  # Corresponds to the errors in the format of the embarques
    for pagina, embarque in zip(paginas, embarques):
        formato_valido = True  # "El formato del embarque es válido"
        embarque_ = {
            "main": None,
            "cost": None,
            "note": None,
        }  # Corresponds to the new elemens of embarques_
        for table in embarque:
            """
            Cada tabla puede ser de tres tipos:
            - Main: Contiene la información principal del embarque
            - Cost: Contiene la información de costos del embarque
            - Note: Contiene notas sobre el embarque
            La tabla de notas es fácil de identificar, siempre dice "Notes" en el nombre de la primera columna y es una única tabla
            El resto de las tablas se identifican por la cantidad de columnas que tienen:
            - Main: >3
            - Cost: 3
            """

            # Verificamos si "Note" está contenido en el inicio del nombre de la primera columna
            if "Note" in table.columns[0][0:5]:
                # Si es así, la tabla es de notas
                embarque_["note"] = table
            # Verificamos si la cantidad de columnas es mayor a 3
            elif len(table.columns) > 3:
                # Si es así, la tabla es de información principal
                # Verificamos si es la primera que se encontró de este tipo
                if type(embarque_["main"]) != pd.DataFrame:
                    if not "Observacion" in table.columns:
                        table["Observacion"] = False
                    # Si es así, la guardamos
                    embarque_["main"] = table
                else:
                    # Si no es la primera, la agregamos a la que ya se encontró
                    table[False] = False
                    embarque_["main"], formato_valido = add_df(embarque_["main"], table)
            # Verificamos si la cantidad de columnas igual a 3
            elif len(table.columns) == 3:
                # Si es así, la tabla es de costos
                # Verificamos si es la primera que se encontró de este tipo
                if type(embarque_["cost"]) != pd.DataFrame:
                    # Si es así, la guardamos
                    embarque_["cost"] = table
                else:
                    # Si no es la primera, la agregamos a la que ya se encontró
                    embarque_["cost"], formato_valido = add_df(embarque_["cost"], table)
            else:
                # Si no es ninguna de las anteriores, el formato no es válido
                formato_valido = False
        # REVISAMOS ERRORES Y CORREGIMOS FORMATO:

        # Revisamos si hay algún elemento de embarque_ no esté definido
        for tipo in ["main", "cost", "note"]:
            if embarque_[tipo] is None:
                formato_valido = False

        # Remplazamos los carriage returns por espacios en los nombres de las columnas de embarque_["main"]
        if formato_valido:
            embarque_["main"].columns = embarque_["main"].columns.str.replace(
                "[\r]", " ", regex=True
            )
            embarque_["main"].columns = [
                col.replace("  ", " ") for col in embarque_["main"].columns
            ]

        # Revisamos que se tengan las columnas válidas en main
        if (
            formato_valido
            and set(main_dict_liq.keys())
            - set(embarque_["main"].columns)
            - {"果园 CSG"}
            - {"Observacion"}
            != set()
        ):
            formato_valido = False

        # Ajustamos el formato de los DataFrame válidos: seleccionamos columnas, cambiasmo nombre de columnas, eliminamos caracteres chinos, establecemos el tipo de elementos de costo como floats
        if formato_valido:
            # Preservamos solo las columnas relevantes en main y le asignamos los nombres deseados
            relevant = list(set(embarque_["main"].columns) & set(main_dict_liq.keys()))
            relevant = sorted(
                relevant, key=lambda x: list(main_dict_liq.keys()).index(x)
            )
            embarque_["main"] = embarque_["main"][relevant]
            # Cambiamos el nombre de las columnas a partir del diccionario
            embarque_["main"] = embarque_["main"].rename(columns=main_dict_liq)

            # Eliminamos caracteres no deseados dentro del df
            embarque_["main"] = df_formatter(embarque_["main"])
            embarque_["cost"] = df_formatter(embarque_["cost"])

            # Remplazamos el nombre de las filas de cost por los valores de su primera columna (luego eliminamos la primera columna)
            embarque_["cost"].index = embarque_["cost"].iloc[:, 0]
            embarque_["cost"] = embarque_["cost"].iloc[:, 1:]
            if not "Total Fees" in embarque_["cost"].index:
                formato_valido = False
            # Verificamos que la tabla de costos tenga las columnas válidas:
            if (
                not "USD" in embarque_["cost"].columns
                or not "RMB" in embarque_["cost"].columns
            ):
                formato_valido = False
            else:
                # Convertimos las columnas que dcorresponden de cost a numéricas
                embarque_["cost"]["RMB"] = pd.to_numeric(
                    embarque_["cost"]["RMB"]
                    .str.replace(",", "")
                    .str.replace(r"\(|\)", "", regex=True)
                    .replace("nan", 0)
                )
                embarque_["cost"]["USD"] = pd.to_numeric(
                    embarque_["cost"]["USD"]
                    .str.replace(",", "")
                    .str.replace(r"\(|\)", "", regex=True)
                    .replace("nan", 0)
                )

        # Extraemos main_summarry y establecemos el fomrato de las columnas de main:
        if formato_valido:
            # Separamos el resumen de main y lo agregamos como un nuevo elemeto del embarque
            embarque_["main_summary"] = embarque_["main_summary"] = (
                embarque_["main"].iloc[-1:].copy()
            )
            embarque_["main_summary"] = embarque_["main_summary"].reset_index(drop=True)
            try:
                embarque_["main_summary"] = embarque_["main_summary"][
                    [
                        "CAJAS LIQUIDADAS",
                        "TOTAL RMB",
                        "TOTAL USD",
                        "RETORNO FOB/CJ",
                        "RETORNO FOB",
                    ]
                ]
                for col in embarque_["main_summary"]:
                    embarque_["main_summary"][col] = pd.to_numeric(
                        embarque_["main_summary"][col].replace(
                            "[^\d.]", "", regex=True
                        ),
                        errors="coerce",
                    )
            except:
                formato_valido = False

        if formato_valido:
            embarque_["main_summary"].index = ["Total"]

            embarque_["main"] = embarque_["main"].iloc[:-1].copy()
            # ESTABLECEMOS EL FORMATO DE LAS COLUMNAS DE MAIN:

            # Replace 'nan' with numpy's representation of NaN
            embarque_["main"] = embarque_["main"].replace("nan", np.nan)
            embarque_["cost"] = embarque_["cost"].replace("nan", np.nan)
            # Eliminamos elementos sin cajas de main
            embarque_["main"] = embarque_["main"].dropna(subset=["CAJAS LIQUIDADAS"])
            # Asignamos valores de los elementos que les pueda faltar
            columns_to_fill = {"KG NET/CAJA", "VARIEDAD", "CALIBRES"}
            for column in columns_to_fill:
                if embarque_["main"][column].isna().any():
                    column_values = embarque_["main"][column].dropna()
                    if len(column_values.unique()) == 1:
                        common_value = column_values.iloc[0]
                        embarque_["main"][column] = embarque_["main"][column].fillna(
                            common_value
                        )
                    elif column == "KG NET/CAJA":
                        formato_valido = False
 
        if formato_valido:
            try:
                # Los pesos como numeros
                embarque_["main"]["KG NET/CAJA"] = embarque_["main"][
                    "KG NET/CAJA"
                ].str.replace(r"[^0-9.]", "", regex=True)
                embarque_["main"]["KG NET/CAJA"] = pd.to_numeric(
                    embarque_["main"]["KG NET/CAJA"], errors="coerce"
                )
                # Las cajas como numeros
                embarque_["main"]["CAJAS LIQUIDADAS"] = embarque_["main"][
                    "CAJAS LIQUIDADAS"
                ].str.replace(r"[^0-9.]", "", regex=True)
                embarque_["main"]["CAJAS LIQUIDADAS"] = pd.to_numeric(
                    embarque_["main"]["CAJAS LIQUIDADAS"], errors="coerce"
                )

                # Las siguientes columnas como números:
                toNumber = [
                    "TOTAL USD",
                    "RMB/CJ",
                    "TOTAL RMB",
                    "RETORNO FOB/CJ",
                    "RETORNO FOB",
                ]
                for column in toNumber:
                    embarque_["main"][column] = embarque_["main"][column].str.replace(
                        "[\$,¥]", "", regex=True
                    )
                    embarque_["main"][column] = pd.to_numeric(
                        embarque_["main"][column].str.replace(",", "")
                    )
                    embarque_["main"][column] = embarque_["main"][column].fillna(0)
            except Exception as e:
                formato_valido = False

        # Si el formato es valido, agregamos el embarque a la lista de embarques, si no, agregamos el error a la lista de errores
        if formato_valido:
            # Agregamos el embarque a la lista de embarques
            embarques_.append(embarque_)
            # Agregamos la pagina a la lista de paginas
            paginas_.append(pagina)
        else:
            # Agregamos el error a la lista de errores
            errores.append(pagina)

    assert len(embarques_) + len(errores) == len(
        embarques
    ), "Se perdieron embarques en el procesamiento"

    return embarques_, errores, paginas_


def feature_engine(embarque: embarqueL) -> None:
    """
    Takes a embarque in the form of an embarqueL and adds columns to the main atribute. The columns added are:

    0) COSTO
    1) COSTO/CJ
    2) COSTO/KG
    3) COMISION
    4) COMISION/CJ
    5) COMISION/KG
    6) COSTO Y COMISION
    7) LIQ FINAL
    8) key

    Args:
        embarque (embarqueL): embarque in the form of an embarqueL

    Returns:
        None

    Raises:
        AssertionError: If embarque is not an instance of embarqueL
    """
    assert isinstance(embarque, embarqueL), "El embarque no es de la clase embarqueL"

    def df_to_str(df: pd.DataFrame) -> str:
        """
        Función que toma un DataFrame y lo convierte a un string uniendo todas las filas y columnas.
        """
        assert isinstance(df, pd.DataFrame), f"El objeto {df} no es un DataFrame"
        df = df.reset_index(drop=True)
        stringed_df = ""
        for column in df.columns:
            stringed_df += str(column) + " "
            for idx, element in enumerate(df[column]):
                if idx == len(df[column]) - 1:
                    stringed_df += str(element) + " "
                else:
                    stringed_df += str(element) + " "

        stringed_df = stringed_df.replace("_x000D_", " ").replace("\n", " ")

        return stringed_df

    # Si todos los elementos de la columan de observacion son False, los cambiamos por la nota.
    # Esto se utiliza para el formato 12Islands
    if (
        embarque.main[embarque.main["Observacion"].isin([False, "False"])].shape
        == embarque.main.shape
    ):
        observacion_str = df_to_str(embarque.note)
        embarque.main["Observacion"] = observacion_str

    # Definimos los costos totales
    fees_index = embarque.cost.index.get_loc("Total Fees")  # Índice de Total Fees
    costo_total = embarque.cost.iloc[:fees_index].sum()  # Total Fees a mano

    # Definimos los kg totales del embarque
    main_Kg = embarque.main.copy()
    main_Kg["KG DE LA FILA"] = main_Kg["KG NET/CAJA"] * main_Kg["CAJAS LIQUIDADAS"]
    kg_totales = main_Kg["KG DE LA FILA"].sum()
    costo_por_kg = costo_total["USD"] / kg_totales

    # Agregamos las columnas de costo
    embarque.main["COSTO"] = (
        embarque.main["KG NET/CAJA"] * costo_por_kg * embarque.main["CAJAS LIQUIDADAS"]
    )
    embarque.main["COSTO/CJ"] = (
        embarque.main["COSTO"] / embarque.main["CAJAS LIQUIDADAS"]
    )
    embarque.main["COSTO/KG"] = costo_por_kg

    # Agregamos la columna de comision
    embarque.main["COMISION"] = embarque.commission * embarque.main["TOTAL USD"]
    embarque.main["COMISION/CJ"] = (
        embarque.main["COMISION"] / embarque.main["CAJAS LIQUIDADAS"]
    )
    embarque.main["COMISION/KG"] = (
        embarque.main["COMISION/CJ"] / embarque.main["KG NET/CAJA"]
    )

    # Establecemos los KG NET/CAJA como strings en un formato compatible con base embarues
    embarque.main["KG NET/CAJA"] = (
        embarque.main["KG NET/CAJA"]
        .astype(float)
        .astype(str)
        .apply(lambda x: x.rstrip("0").rstrip("."))
    )

    # Agregamos columna COSTO Y COMISION
    embarque.main["COSTO Y COMISION"] = (
        embarque.main["COMISION"] + embarque.main["COSTO"]
    )

    # Agregamos la scolumna LIQ FINAL
    embarque.main["LIQ FINAL"] = embarque.main["TOTAL USD"] - (
        embarque.main["COSTO"] + embarque.main["COMISION"]
    )


# ARREGLAR COMENTARIO INTRODUCTORIO
def liquidaciones(
    folder: str, update_loading_bar: callable = None, total_operations: int = None
) -> tuple[list, dict, dict]:
    """
    Recieves a path to an Excel file or PDF file containing the liquidactions in the format of Happy Farm Fruit, Jumbo Fruit, 12Islands, or standard.
    The function returns a tuple with three coordinates:
    Returns a tuple:

    0) A list of embarqueL, the n-th element of the list is an embarqueL corresponding to the n-th embarque in folder.
    1) A dictionary, the keys are the names of the PDFs in folder and the values are lists of integers corresponding to the first page of the embarques where errors where found.
    2) A dictonary, the keys are tuples with the name of the PDF and the page number of the error and the values are the errors, as a list, found in the format of the embarques.

    Args:
        liquidaciones (list): List of lists of DataFrames

    Returns:
        tuple: tuple with two coordinates (list, dict, dict)

    Raises:
        AssertionError: If the path does not exist
        AssertionError: If the path is not a PDF file
    """

    assert os.path.exists(folder), f"La ruta del archivo {folder} no existe."

    # Creamos la lista de embarques y de errores
    embarques = []
    errores = {}
    ubicaciones = []

    def procesarLiquidacionYAlmacenarDatos(liquidacion: str) -> None:
        """
        Recibe un string con el path de una liquidación y la interpreta y luego agrupa considerando errores y registrando la página inicial de cada embarque.
        """
        # Creamos una key que distingue el archivo
        key = os.path.basename(liquidacion)
        key = os.path.splitext(key)[0]
        # obtenemos el path completo
        liquidacion = os.path.join(folder, liquidacion)

        # Importamos y ordenamos las tablas
        try:
            embarque, paginas = interpreter(liquidacion)
            # Ajustamos el fomrato de cada lista de la lista embaruqes tal que tenga 5 DataFrames correspondiendo al "main", "cost", "note", "main_summary"
            embarque, error, paginas = embarques_three_tables(embarque, paginas)
            ubicacion = [(key, pagina) for pagina in paginas]
            ubicaciones.extend(ubicacion)
            embarques.extend(embarque)
        except Exception as e:
            if liquidacion.endswith((".xls", ".xlsx")):
                error = [1]
            else:
                error = ["Todas las páginas"]

        errores[key] = error

    if os.path.isdir(folder):
        for liquidacion in os.listdir(folder):
            procesarLiquidacionYAlmacenarDatos(liquidacion)
            if update_loading_bar:  # liquidacion operacion
                update_loading_bar(1 / total_operations * 100)

    else:
        assert os.path.isfile(
            folder
        ), f"La ruta del archivo {folder} no es un archivo ni una carpeta."
        procesarLiquidacionYAlmacenarDatos(folder)
        if update_loading_bar:  # liquidacion operacion
            update_loading_bar(1 / total_operations * 100)

    assert len(ubicaciones) == len(
        embarques
    ), "La cantidad de ubicaciones no coincide con la cantidad de embarques"

    # Guardamos los embarques en forma de la clase embarqueL
    # Creamos en cada embarque las columnas con los keys para el merge
    embarques_ = []  # la lista con los embarques como clase
    revisar = {}
    for embarque, ubicacion in zip(embarques, ubicaciones):
        # Guardamos el embarque como una instancia de embarqueL
        embarque = embarqueL(
            embarque["main"],
            embarque["cost"],
            embarque["note"],
            embarque["main_summary"],
            ubicacion,
        )

        # Revisamos el embarque
        hay_inconsistencias, inconsistencias = revisar_liquidacion(embarque)
        if hay_inconsistencias:
            revisar[ubicacion] = inconsistencias

        # Verificamos si el embarque tiene columna de CSG
        embarque.CSG = "CSG" in embarque.main.columns  # "El embarque tiene columna CSG"

        # Agregamos las columnas pertinentes
        feature_engine(embarque)

        # Solo mayusculas en los valores de las columnas key (y en formato str)
        keys = key_liq if embarque.CSG else key_liq_incompleto
        for key in keys:
            embarque.main[key] = embarque.main[key].astype(str).str.upper()

        # Agregamos el embarque a la lista de embarques_
        embarques_.append(embarque)

    return embarques_, errores, revisar


if __name__ == "__main__":
    embarques, errores, revisar = liquidaciones(liquidacion)

    if len(embarques) > 0:
        print("Main del último embarque:")
        print(embarques[-1].main)
        print()
        print("Cost del último embarque:")
        print(embarques[-1].cost)
        print()
        print("Note del último embarque:")
        print(embarques[-1].note)
        print()
        print("Resumen de main del último embarque:")
        print(embarques[-1].main_summary)
        print()
    else:
        print("Ningún embarque se pudo leer correctamente")
        print()

    print("Errores totales:")
    print(errores)
    print()
    print("Por revisar:")
    print(revisar)
