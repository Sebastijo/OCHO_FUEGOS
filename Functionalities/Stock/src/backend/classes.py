import numpy as np
import pandas as pd
from pathlib import Path


class Material:
    """
    A class to represent a material.

    Attributes
    ----------
    name : str
        the name of the material
    stock : int
        the current stock of the material
    emergency_stock : int
        the emergency stock of the material, ideally never reached.
    delivery_time : int
        the delivery time of the material
    minimum_stock : int
        the minimum stock of the material, if this point is reached, the material should be ordered.
    maximum_stock : int
        the maximum stock of the material, this is the level the stock should be refilled to.
    order_amount : int
        the amount of material that should be ordered.
    rate_of_change : int
        the rate of change of the stock, measured in units per day.
    history : dict[str, list]
        a dictionary with the history of the stock, minimum stock, maximum stock and arrived stock.

    Methods
    -------
    enough_stock()
        returns a boolean indicating if the stock is above the minimum stock.
    step(boxes_needed: dict[str, float], usage_per_box_type: dict[str, float])
        updates the rate of change, minimum stock and maximum stock of the material.
    reset_history()
        resets the history of the material.
    round_values()
        rounds the values of the stock, minimum stock and maximum stock.
    __str__()
        returns a string representation of the material.
    """

    def __init__(self, name: str, stock: int, emergency_stock: int, delivery_time: int):

        self.history: dict[str, list] = {
            "stock": [],
            "minimum_stock": [],
            "maximum_stock": [],
            "arrived_stock": []
        }
        self.name = name
        self.stock = stock
        self.emergency_stock = emergency_stock  # measured in units
        self.delivery_time = delivery_time  # measured in days

        self.minimum_stock = float("inf")  # when to order more
        self.maximum_stock = float("inf")  # refill to this level
        self.order_amount = float("inf")  # amount to order
        self.rate_of_change = float("inf")  # measured in units per day

    @property
    def enough_stock(self):
        return self.stock > self.minimum_stock - 0.5 * self.rate_of_change

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

        # Update order ammount
        self.order_amount = self.maximum_stock - self.emergency_stock
        # How much should be minus how much will be

        # Store in history
        self.history["stock"].append(self.stock)
        self.history["minimum_stock"].append(self.minimum_stock)
        self.history["maximum_stock"].append(self.maximum_stock)

    def reset_history(self):
        self.history = {
            "stock": [],
            "minimum_stock": [],
            "maximum_stock": [],
            "arrived_stock": []
        }

    def round_values(self):
        self.stock = round(self.stock)
        self.minimum_stock = round(self.minimum_stock)
        self.maximum_stock = round(self.maximum_stock)
        self.order_amount = round(self.order_amount)

    def __str__(self):
        return f"{self.name}: {self.stock} unidades/ {self.minimum_stock} min/ {self.maximum_stock} max"


class Packing:
    """
    A class to represent a packing.

    Attributes
    ----------
    name : str
        the name of the packing
    materials : np.array[Material]
        the materials that are packed in this packing
    kg2box : pd.DataFrame
        a dataframe with the conversion from kg to boxes
    box2material : dict[str, pd.DataFrame]
        a dictionary with the conversion from boxes to materials

    Methods
    -------
    populate(materials: pd.DataFrame)
        populates the materials attribute with the given dataframe.
    update_minimum_and_maximum_stocks(kg: float)
        updates the minimum and maximum stocks of the materials in the packing.
    round_values()
        rounds the stock values of the materials in the packing.
    update_stocks(new_stocks: pd.DataFrame)
        updates the stock values of the materials in the packing.
    reset_history()
        resets the history of the materials in the packing.
    __str__()
        returns a string representation of the packing.
    """

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
        for material in self:
            material.round_values()

    def update_stocks(self, new_stocks: pd.DataFrame):
        for material in self:
            material.stock = new_stocks.loc[
                new_stocks["CODIGO"] == material.name, "STOCK"
            ].values[0]

    def reset_history(self):
        for material in self:
            material.reset_history()

    def __str__(self):
        output = f"{self.name}:\n"
        for material in self:
            output += f"{material}\n"
        return output
