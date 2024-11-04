import numpy as np
import pandas as pd
from pathlib import Path


class Material:
    """
    A class to represent a material.
    """

    def __init__(self, name: str, stock: int, emergency_stock: int, delivery_time: int):

        self.history: dict[str, list] = {
            "stock": [],
            "minimum_stock": [],
            "maximum_stock": [],
        }
        self.name = name
        self.stock = stock
        self.emergency_stock = emergency_stock  # measured in units
        self.delivery_time = delivery_time  # measured in days

        self.minimum_stock = float("inf")  # when to order more
        self.maximum_stock = float("inf")  # refill to this level
        self.rate_of_change = float("inf")  # measured in units per day

    @property
    def enough_stock(self):
        return self.stock > self.minimum_stock

    def step(
        self, boxes_needed: dict[str, float], usage_per_box_type: dict[str, float]
    ):
        # Update rate of change
        self.rate_of_change = 0
        for box_type, boxes_of_type in boxes_needed.items():
            self.rate_of_change -= (boxes_of_type * usage_per_box_type[box_type]) / 7

        # Update minimum stock
        self.minimum_stock = (
            self.emergency_stock - self.rate_of_change * self.delivery_time
        )  # S(x) = c - S'(x) * t (is a first order taylor for S(x+d) = c)

        # Update maximum stock
        self.maximum_stock = self.emergency_stock - self.rate_of_change * 7
        # S(x+d) = c - S'(x+d) * 7 (is a first order taylor for S(x+d+7) = c)

        # Store in history
        self.history["stock"].append(self.stock)
        self.history["minimum_stock"].append(self.minimum_stock)
        self.history["maximum_stock"].append(self.maximum_stock)

    def reset_history(self):
        self.history = {
            "stock": [],
            "minimum_stock": [],
            "maximum_stock": [],
        }

    def __str__(self):
        return f"{self.name}: {self.stock} unidades/ {self.minimum_stock} min/ {self.maximum_stock} max"


class Packing:
    def __init__(
        self,
        name: str,
        materials: pd.DataFrame,
        kg2box: pd.DataFrame,
        box2material: dict[str, pd.DataFrame],
    ):
        self.name: str = name
        self.populate(materials)  # This defines self.materials
        self.kg2box: pd.DataFrame = kg2box
        self.box2material: dict[str, pd.DataFrame] = box2material

        self.index: int = 0
        self.boxes_needed: dict[str, float] = (
            {}
        )  # weekly boxes needed by box type (for current week).
        self.w_kg: float = 0  # expected kg used in the current week.

    def __iter__(self):
        # Reset the index for a new iteration
        self.index = 0
        return self

    def __next__(self):
        if self.index < len(self.materials):
            material = self.materials[self.index]
            self.index += 1
            return material
        else:
            raise StopIteration

    def populate(self, materials: pd.DataFrame):
        self.materials = np.empty(len(materials), dtype=Material)
        for i in range(len(materials)):
            element: dict = materials.iloc[i]
            material = Material(
                element["CODIGO"],
                element["STOCK"],
                element["EMERGENCY STOCK"],
                element["DELIVERY TIME"],
            )
            self.materials[i] = material

    def update_minimum_and_maximum_stocks(self, kg: float):
        self.w_kg = kg

        # Get the boxes needed, by type, for the current week.
        self.boxes_needed: dict[str, float] = {}
        for _, row in self.kg2box.iterrows():
            box_type = row["BOX TYPE"]
            boxes_per_10kg = row["BOXES PER 10KG"]
            self.boxes_needed[box_type] = (kg / 10) * boxes_per_10kg

        item = lambda df: df.values[0] if len(df) > 0 else 0
        b2m: dict[str, pd.DataFrame] = self.box2material
        for material in self:
            usage_per_box_type = {
                box_type: item(
                    b2m[box_type].loc[
                        b2m[box_type]["CODIGO"] == material.name, "X CAJA"
                    ]
                )
                for box_type in self.boxes_needed.keys()
            }
            material.step(self.boxes_needed, usage_per_box_type)

    def round_values(self):
        for material in self.materials:
            material.stock = round(material.stock)
            material.minimum_stock = round(material.minimum_stock)
            material.maximum_stock = round(material.maximum_stock)

    def update_stocks(self, new_stocks: pd.DataFrame):
        for material in self.materials:
            material.stock = new_stocks.loc[
                new_stocks["CODIGO"] == material.name, "STOCK"
            ].values[0]

    def reset_history(self):
        for material in self.materials:
            material.reset_history()

    def __str__(self):
        output = f"{self.name}:\n"
        for material in self.materials:
            output += f"{material}\n"
        return output
