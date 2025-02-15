import tkinter as tk
from tkinter import ttk

class ManageCompany:
    def __init__(self, parent):
        self.parent = parent

    def display(self):
        label = tk.Label(self.parent, text="Manage Company", font=("Arial", 16))
        label.pack(pady=20)

        tree = ttk.Treeview(self.parent, columns=("ID", "Name", "Country"), show="headings")
        tree.heading("ID", text="Company ID")
        tree.heading("Name", text="Name")
        tree.heading("Country", text="Country")

        # Example data
        data = [(1, "Space Systems", "Poland"), (2, "Rocket Inc.", "USA")]
        for row in data:
            tree.insert("", "end", values=row)

        tree.pack(fill="both", expand=True)
