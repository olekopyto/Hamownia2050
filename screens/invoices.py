from tkinter import ttk
import tkinter as tk

class Invoices:
    def __init__(self, parent):
        self.parent = parent

    def display(self):
        tree = ttk.Treeview(self.parent, columns=("ID", "Amount", "Date"), show="headings")
        tree.heading("ID", text="Invoice ID")
        tree.heading("Amount", text="Amount")
        tree.heading("Date", text="Date")

        # Dummy data
        data = [(1, "$1000", "2025-01-01"), (2, "$500", "2025-01-10")]
        for row in data:
            tree.insert("", "end", values=row)

        tree.pack(fill="both", expand=True)
