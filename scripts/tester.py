import pandas as pd

data = {
    "Category": ["A", "B", "A", "B", "A", "B"],
    "Type": ["Y", "Y", "X", "Y", "X", "Y"],
    "CAJAS": [10, 20, 15, 25, 12, 18],
}

df = pd.DataFrame(data)

key_liq = ["Category", "Type"]


def simplifier(pseudocontrol: pd.DataFrame) -> pd.DataFrame:
    """
    Recibe un (DataFrame del tipo entregado por la función) pseudoControl y devuelve el DataFrame con los siguientes cambios:
    - Deja un único elemento por cada key_liq (elimina los duplicados).
    - El representante de cada key_liq, en cada feature donde haya habido una diferencia entre los duplicados, se convierte a una tupla con el valor de la columna de cada representante.
    - La cantidad de cajas, "CAJAS", siempre es una tupla con la cantidad de cajas de cada representante.
    - Se agrega una columna a la derecha de "CAJAS", "CAJAS TOTALES", con la suma de las cajas de cada representante.

    Args:
        df (pd.DataFrame): DataFrame del tipo entregado por la función pseudoControl.

    Returns:
        pd.DataFrame: DataFrame con los cambios especificados.

    Raises:
        AssertionError: Si el input no es un DataFrame.
    """
    assert isinstance(
        pseudocontrol, pd.DataFrame
    ), f"El input '{pseudocontrol}' no es un DataFrame. En la función 'simplifier'. No se pudieron unir los pallets repetidos."

    def unioner(df):
        """
        Recibe un DataFrame y lo reduce a un solo representante (fila). Si hay diferencias entre los representantes, estas se convierten a tuplas.
        Si existe una columna con el nombre "CAJAS", la columna siempre se convierte en una tupla con la canidad de cajas de cada representante.
        """
        simp_df_data = {}
        # Reducimos todas las filas a una sola fila, con cada elemento, de haber diferencias o ser CAJAS, convertido a una tupla.
        for column in df.columns:
            value = tuple(df[column].tolist())
            if (column != "CAJAS" and all(elem == value[0] for elem in value)) or len(
                value
            ) == 1:
                value = value[0]
            simp_df_data[column] = [value]
        simp_df = pd.DataFrame(simp_df_data)

        return simp_df

    # Reducimos el DataFrame a un solo representante por key_liq
    pseudocontrol = pseudocontrol.groupby(key_liq).apply(unioner).reset_index(drop=True)

    return pseudocontrol

pseudo_control = simplifier(df)

print(pseudo_control)