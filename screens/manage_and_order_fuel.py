from tkinter import ttk
import tkinter as tk

class ManageAndOrderFuel:
    def __init__(self, parent):
        self.parent = parent

    def display(self):
        label = ttk.Label(self.parent, text="Manage and Order Fuel", font=("Arial", 16))
        label.pack(pady=20)

        # Add controls to manage fuel
        tree = ttk.Treeview(self.parent, columns=("ID", "Fuel Type", "Quantity"), show="headings")
        tree.heading("ID", text="Fuel ID")
        tree.heading("Fuel Type", text="Fuel Type")
        tree.heading("Quantity", text="Available Quantity (L)")

        # Example data
        data = [
            (1, "Kerosene", "1000"),
            (2, "Liquid Oxygen", "500"),
        ]
        for row in data:
            tree.insert("", "end", values=row)

        tree.pack(fill="both", expand=True)
