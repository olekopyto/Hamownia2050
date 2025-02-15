import tkinter as tk


class RegisterCompany:
    def __init__(self, parent):
        self.parent = parent

    def display(self):
        frame = tk.Frame(self.parent)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="Company Name:").grid(row=0, column=0, sticky="e")
        tk.Entry(frame).grid(row=0, column=1)
        tk.Label(frame, text="Country:").grid(row=1, column=0, sticky="e")
        tk.Entry(frame).grid(row=1, column=1)

        tk.Button(frame, text="Register").grid(row=2, columnspan=2, pady=10)
