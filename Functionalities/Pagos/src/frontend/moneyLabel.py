"""
A class for the amount of money each client has in the pagos program.
"""

import tkinter as tk


class MoneyLabel:
    def __init__(
        self,
        frame: tk.Frame,
        cliente: str,
        bg: str,
        fg: str,
        initial_payed: int = 0,
        initial_used: int = 0,
        initial_net: int = 0,
    ):

        self.cliente = cliente

        # Create an IntVar for the money value
        self.payed_var = tk.IntVar(value=initial_payed)
        self.used_var = tk.IntVar(value=initial_used)
        self.net_var = tk.IntVar(value=initial_net)

        # Create a StringVar to hold the formatted display string
        self.money_label_var = tk.StringVar()

        # Trace changes to the IntVar
        self.net_var.trace("w", self.update_label) # update_label will be called when the net_var changes

        # Initialize the label text
        self.update_label()

        # Create the Label widget
        self.label = tk.Label(frame, textvariable=self.money_label_var, bg=bg, fg=fg)

    def update_label(self, *args):
        # Format the value with a dollar sign
        self.money_label_var.set(
            f"{self.cliente}: ${self.payed_var.get():,} pagado / ${self.used_var.get():,} utilizado / ${self.net_var.get():,} restante".replace(",", ".")
        )

    def set_value(self, payed: int, used: int, net: int):
        """
        Function for setting the value of the money label.

        Args:
            payed (int): The amount of money payed by the client.
            used (int): The amount of money used by the client.
            net (int): The net amount of money the client has.
        """
        # Update the money_var, which will trigger the label update
        self.payed_var.set(payed)
        self.used_var.set(used)
        self.net_var.set(net) # needs to be updated last

    def get_value(self):
        # Retrieve the current value
        pagado = self.payed_var.get()
        utilizado = self.used_var.get()
        restante = self.net_var.get()
        return pagado, utilizado, restante

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
