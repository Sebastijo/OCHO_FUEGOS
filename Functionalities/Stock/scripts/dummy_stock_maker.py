import pandas as pd
import random
from pathlib import Path

data_dir = Path(__file__).resolve().parents[1] / "data"  # Path to the data directory
dummy_stock_path = data_dir / "dummy_stock.xlsx"  # Path to the dummy stock data
dummy_stock_limits_path = (
    data_dir / "dummy_stock_limits.xlsx"
)  # Path to the dummy stock limits data

# we set the seed
random.seed(115)

# Create a dummy stock data

item_names = [
    "MCER017",
    "MCER018",
    "MCER020",
    "MCER021",
    "MCER022",
    "MCER026",
    "MCER027",
    "MCER028",
    "MCER029",
    "MCER030",
    "MCER031",
    "MCER032",
    "MCER033",
    "MCER034",
    "MCER035",
    "MCER036",
    "MCER037",
    "MCER038",
    "MCER039",
    "MCER040",
    "MCER041",
    "MCER043",
    "MCER046",
    "MCER047",
    "MCER051",
    "MCER057",
    "MCER067",
]

ammount_of_items: int = len(item_names)

print("Item ammount: ", ammount_of_items)

items: list[str] = item_names
stock1: list[int] = [random.randint(1, 1000) for i in range(len(items))]
stock2: list[int] = [random.randint(1, 1000) for i in range(len(items))]
minimum_stock1: list[int] = [random.randint(1, 100) for i in range(len(items))]
maximum_stock1: list[int] = [random.randint(100, 1000) for i in range(len(items))]
minimum_stock2: list[int] = [random.randint(1, 100) for i in range(len(items))]
maximum_stock2: list[int] = [random.randint(100, 1000) for i in range(len(items))]

stock_data1: pd.DataFrame = pd.DataFrame(
    {
        "item": items,
        "stock": stock1,
    }
)

stock_data2: pd.DataFrame = pd.DataFrame(
    {
        "item": items,
        "stock": stock2,
    }
)

stock_limits1: pd.DataFrame = pd.DataFrame(
    {
        "item": items,
        "minimum_stock": minimum_stock1,
        "maximum_stock": maximum_stock1,
    }
)

stock_limits2: pd.DataFrame = pd.DataFrame(
    {
        "item": items,
        "minimum_stock": minimum_stock2,
        "maximum_stock": maximum_stock2,
    }
)

print(stock_data1)
print(stock_limits1)

with pd.ExcelWriter(dummy_stock_path) as writer:
    stock_data1.to_excel(writer, index=False, sheet_name="packing_0")
    stock_data2.to_excel(writer, index=False, sheet_name="packing_1")

with pd.ExcelWriter(dummy_stock_limits_path) as writer:
    stock_limits1.to_excel(writer, index=False, sheet_name="packing_0")
    stock_limits2.to_excel(writer, index=False, sheet_name="packing_1")

print("Dummy stock data created successfully.")
