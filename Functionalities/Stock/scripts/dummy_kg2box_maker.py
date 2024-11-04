"""
this module's objective is to create a dummy kg to box converter
"""

import pandas as pd
import random
from pathlib import Path

data_dir = Path(__file__).resolve().parents[1] / "data"  # Path to the data directory
dummy_stock_path = data_dir / "dummy_kg2box.xlsx"  # Path to the dummy stock data

# we set the seed
random.seed(115)

# Create a dummy stock data
my_box_types = ["CGA8F1", "CGM8F1", "CGM8F", "PGMC2", "PGMCJ"]

ammount_of_box_types: int = len(my_box_types)

box_types: list[str] = my_box_types
# the information will be provided in how many boxes will be made with 10 kg of cherries
# that arrive at the packing.
boxes_per_10kg: list[int] = [random.randint(1, 6) for i in range(len(box_types))]

stock_data: pd.DataFrame = pd.DataFrame(
    {
        "BOX TYPE": box_types,
        "BOXES PER 10KG": boxes_per_10kg,
    }
)

print(stock_data)

with pd.ExcelWriter(dummy_stock_path) as writer:
    stock_data.to_excel(writer, index=False, sheet_name="kg2box")

print(f"Dummy kg2box data created at {dummy_stock_path}")
