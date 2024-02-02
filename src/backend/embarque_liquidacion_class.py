"""
The objective of this module is to define a class that represents the 12 Island liquidation file. This will be done through three different pandas DataFrames
Empresa: Ocho Fuegos
Autor: Sebastián P. Pincheira
Fecha: 05/01/2024
Lenguaje: Python 3.11.7
Librerías:
- pandas: 2.2.0
"""
import pandas as pd
import re


class embarqueL:
    def __init__(
        self,
        main: pd.DataFrame,
        cost: pd.DataFrame,
        note: pd.DataFrame,
        main_summary: pd.DataFrame,
        location: tuple,
    ) -> None:
        self.main = main
        self.cost = cost
        self.note = note
        self.main_summary = main_summary
        self.location = location
        self.commission = 0.0
        self.commission_value = 0.0
        for idx in self.cost.index:
            match = re.search(r"\(([\d.]+)%\)", idx)
            if match:
                self.commission = float(match.group(1)) / 100
                self.commission_value = float(
                    str(self.cost.at[idx, "USD"]).replace("$", "")
                )
                break

        self.CSG = None


if __name__ == "__main__":
    # Sample DataFrame for "main"
    main_data = {"A": [1, 2, 3], "B": [4, 5, 6]}
    main_df = pd.DataFrame(main_data)

    # Sample DataFrame for "cost" with "Commission (8%)" in the index
    cost_data = {"RMB": [10, 20, 30], "USD": [1, 2, 3]}
    cost_index = ["Item 1", "Item 2", "Commission (8%)"]
    cost_df = pd.DataFrame(cost_data, index=cost_index)

    # Sample DataFrame for "note"
    note_data = {"Note": ["Note 1", "Note 2", "Note 3"]}
    note_df = pd.DataFrame(note_data)

    # Sample DataFrame for "main_summary"
    main_summary_data = {"Summary": ["Summary 1", "Summary 2", "Summary 3"]}
    main_summary_df = pd.DataFrame(main_summary_data)

    # Sample location
    location = ("location", 0)

    # Test your class with these DataFrames
    test = embarqueL(main_df, cost_df, note_df, main_summary_df, location)

    print(test.main)
    print(test.cost)
    print(test.main_summary)
    print(test.commission)
    print(test.commission_value)
