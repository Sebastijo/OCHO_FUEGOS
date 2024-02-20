import sympy as sp
from decimal import Decimal
import numpy as np
import pandas as pd

column_to_test = pd.DataFrame(
    {
        "规格 Specification": [
            "3*2.5KG",
            "2*2.5KG",
            "2*2.5KG",
            "2*2.5KG",
            "2*2.5KG",
            "2*2.5KG",
            "2*2.5KG",
            "2*2.5KG",
            "2*2.5KG",
            "2*2.5KG",
            "2*2.5KG",
            "3*2.5KG",
            "5KG",
            "5KG",
            "5KG",
            "5KG",
            "5KG",
            "5KG",
            "5KG",
            "5KG",
            "2.5KG",
            "3",
            np.nan,
            np.nan,
        ]
    }
)


def simplifier_for_dataFrame(columns: pd.DataFrame) -> pd.DataFrame:
    return columns.apply(simplifier)

def simplifier(x):
    """
    Takes a string x of the form f"{expression}KG" and return f"{simplified}KG"
    Example: simplifier("2*2.5KG") -> "5KG"

    Args:
        x (str): The string to be simplified

    Returns:
        str: The simplified string
    """
    if isinstance(x, str):
        # Extract the expression from the string
        expression = x.split("KG")[0]
        # Simplify the expression
        simplified = sp.simplify(expression)
        # Convert the simplified expression to Decimal
        simplified_decimal = Decimal(str(simplified))
        # Remove unnecessary decimal places
        simplified_decimal = simplified_decimal.normalize()
        # Convert back to string
        simplified_str = str(simplified_decimal)
        # Return the simplified expression
        return f"{simplified_str}KG"
    else:
        return np.nan if np.isnan(x) else str(x)

# Test the function
simplified_column = simplifier_for_dataFrame(column_to_test["规格 Specification"])
print(simplified_column)
print(simplifier("1.25KG"))  # 1.25KG
print(simplifier("5"))  # 2.5KG
print(simplifier("3"))  # 3KG


print(simplified_column)