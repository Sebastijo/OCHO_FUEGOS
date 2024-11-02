import numpy as np
import pandas as pd
from pathlib import Path


class Material:
    def __init__(self, name: str, stock: int):
        self.name = name
        self.stock = stock
        self.minimum_stock = float("inf")
        self.maximum_stock = float("inf")
        self.rate_of_ussage = 0  # measured in units per day

    @property
    def enough_stock(self):
        return self.stock > self.minimum_stock

    def set_limits(self, minimum_stock: int, maximum_stock: int):
        self.minimum_stock = minimum_stock
        self.maximum_stock = maximum_stock

    def __str__(self):
        return f"{self.name}: {self.stock} units"


class Packing:
    def __init__(self, name: str, materials: np.ndarray[Material]):
        self.name: str = name
        self.materials: np.ndarray[Material] = materials
        self.boxes_needed: dict[str, float] = {}  # weekly boxes needed by box type.

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

    def update_rate_of_use(self, kg: float, kg2box: pd.DataFrame):
        self.boxes_needed = kg_to_boxes(kg, kg2box)
        box2material(self.boxes_needed, box2material, self)

    def __str__(self):
        df = pd.DataFrame([material.__dict__ for material in self.materials])
        return f"{self.name}: {df.to_string(index=False)}"


def kg_to_boxes(kg: float, kg2box: pd.DataFrame) -> dict[str, float]:
    """
    Converts the amount of cherries in kg to the amount of boxes needed for each box type.

    Args:
        kg (float): The amount of cherries in kg.
        kg2box (pd.DataFrame): The relationship between kg and boxes.

    Returns:
        dict[str, float]: The amount of boxes needed for each box type.
    """

    boxes_needed: dict[str, float] = {}

    for _, row in kg2box.iterrows():
        box_type = row["box_type"]
        boxes_per_10kg = row["boxes_per_10kg"]
        boxes_needed[box_type] = (kg / 10) * boxes_per_10kg

    return boxes_needed


def get_rate_of_use(
    boxes_needed: dict[str, float],
    box2material: dict[str, pd.DataFrame],
    packing: Packing,
) -> dict[str, float]:
    """
    Updates the rate of use of each material in the packing.
    The unit of measure of the rate is units per day.

    Args:
        boxes_needed (dict[str, float]): The boxes needed for each box type for the week.
        box2material (dict[str, pd.DataFrame]): The box to material relationship.
        packing (Packing): The packing to update.

    Returns:
        dict[str, float]: The rate of use of each material.
    """

    assert isinstance(boxes_needed, dict)
    assert isinstance(box2material, dict)
    assert isinstance(packing, Packing)

    assert set(boxes_needed.keys()) == set(box2material.keys()), "keys don't match"

    for material in packing:
        for box_type, boxes_of_type in boxes_needed.items():
            b2m = box2material[box_type]
            usage_per_box = b2m.loc[b2m["material"] == material.name, "X Caja"].values[
                0
            ]
            material.rate_of_ussage += (boxes_of_type * usage_per_box) / 7
