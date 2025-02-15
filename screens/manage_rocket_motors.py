from tkinter import ttk
import tkinter as tk

class ManageRocketMotors:
    def __init__(self, parent):
        self.parent = parent

    def display(self):
        label = ttk.Label(self.parent, text="Manage Rocket Motors", font=("Arial", 16))
        label.pack(pady=20)

        # Add controls to manage rocket motors
        tree = ttk.Treeview(self.parent, columns=("ID", "Model", "Thrust"), show="headings")
        tree.heading("ID", text="Motor ID")
        tree.heading("Model", text="Model")
        tree.heading("Thrust", text="Thrust (kN)")

        # Example data
        data = [
            (1, "RM-1", "500"),
            (2, "RM-2", "750"),
        ]
        for row in data:
            tree.insert("", "end", values=row)

        tree.pack(fill="both", expand=True)
