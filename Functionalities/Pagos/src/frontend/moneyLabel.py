"""
A class for the amount of money each client has in the pagos program.
"""
import tkinter as tk

class MoneyLabel:
    def __init__(
        self, frame: tk.Frame, cliente: str, bg: str, fg: str, initial_value: int = 0
    ):

        self.cliente = cliente

        # Create an IntVar for the money value
        self.money_var = tk.IntVar(value=initial_value)

        # Create a StringVar to hold the formatted display string
        self.money_label_var = tk.StringVar()

        # Trace changes to the IntVar
        self.money_var.trace("w", self.update_label)

        # Initialize the label text
        self.update_label()

        # Create the Label widget
        self.label = tk.Label(frame, textvariable=self.money_label_var, bg=bg, fg=fg)

    def update_label(self, *args):
        # Format the value with a dollar sign
        self.money_label_var.set(f"{self.cliente}: ${self.money_var.get()}")

    def set_value(self, value):
        # Update the money_var, which will trigger the label update
        self.money_var.set(value)

    def get_value(self):
        # Retrieve the current value
        return self.money_var.get()

    def add_value(self, value):
        # Add a value to the current value
        self.money_var.set(self.money_var.get() + value)

    def grid(self, **kwargs):
        self.label.grid(**kwargs)

    def pack(self, **kwargs):
        self.label.pack(**kwargs)

    def place(self, **kwargs):
        self.label.place(**kwargs)

    def destroy(self):
        self.label.destroy()