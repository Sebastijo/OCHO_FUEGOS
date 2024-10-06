import pandas as pd
import random
from pathlib import Path

data_dir = Path(__file__).resolve().parents[1] / "data"  # Path to the data directory
dummy_stock_path = data_dir / "dummy_stock.xlsx"  # Path to the dummy stock data

# we set the seed
random.seed(115)

# Create a dummy stock data

items: list[str] = ["item1", "item2", "item3", "item4", "item5"]
stock: list[int] = [random.randint(1, 1000) for i in range(len(items))]
minimum_stock: list[int] = [random.randint(1, 100) for i in range(len(items))]
maximum_stock: list[int] = [random.randint(100, 1000) for i in range(len(items))]

stock_data: pd.DataFrame = pd.DataFrame(
    {
        "item": items,
        "stock": stock,
        "minimum_stock": minimum_stock,
        "maximum_stock": maximum_stock,
    }
)

print(stock_data)

# Save the dummy stock data to the data directory
stock_data.to_excel(dummy_stock_path, index=False)
