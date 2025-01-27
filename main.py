import tkinter as tk
from tkinter import ttk
import psycopg2
from sshtunnel import SSHTunnelForwarder

# Read setup data from file
with open("pass.conf", "r") as f:
    lines = f.read().splitlines()
    SSH_USER = lines[0]  # 1st line of pass.conf
    SSH_PASS = lines[1]  # 2nd line of pass.conf
    DB_USER = lines[2]   # 3rd line of pass.conf
    DB_PASS = lines[3]   # 4th line of pass.conf

# SSH and Database connection setup
SSH_HOST = "pascal.fis.agh.edu.pl"
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "u2kopyto"  # Replace with your actual database name

ssh_tunnel = None
current_user = None

def connect_to_db():
    global ssh_tunnel
    try:
        # Set up SSH tunnel
        ssh_tunnel = SSHTunnelForwarder(
            (SSH_HOST, 22),
            ssh_username=SSH_USER,
            ssh_password=SSH_PASS,
            remote_bind_address=(DB_HOST, DB_PORT),
            local_bind_address=("localhost", DB_PORT)
        )
        ssh_tunnel.start()

        # Connect to the database
        conn = psycopg2.connect(
            host="localhost",
            port=ssh_tunnel.local_bind_port,
            user=DB_USER,
            password=DB_PASS,
            dbname=DB_NAME
        )
        return conn
    except Exception as e:
        print("Error connecting to database:", e)
        if ssh_tunnel:
            ssh_tunnel.stop()
        return None

# Left column elements
def get_elements():
    if current_user == "Space Systems":
        return [
            {"name": "Manage Company", "access": 2},
            {"name": "Manage Rocket Motors", "access": 1},
            {"name": "Manage and Order Fuel", "access": 1},
            {"name": "Invoices", "access": 0},
            {"name": "Register Company", "access": 2},
        ]
    else:
        return [
            {"name": "Invoices", "access": 0},
        ]

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rocket Engine Test Center GUI")

        # Frames for layout
        self.left_frame = tk.Frame(self.root, width=200, bg="lightgray")
        self.middle_frame = tk.Frame(self.root, width=600, bg="white")
        self.right_frame = tk.Frame(self.root, width=200, bg="gray")

        self.left_frame.grid(row=0, column=0, sticky="nswe")
        self.middle_frame.grid(row=0, column=1, sticky="nswe")
        self.right_frame.grid(row=0, column=2, sticky="nswe")

        # Configure column and row weights
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=3)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # Populate left column
        self.populate_left()

        # Placeholder for middle content
        self.middle_label = tk.Label(self.middle_frame, text="Select an option from the left panel.", font=("Arial", 14))
        self.middle_label.pack(expand=True)

        # Right column connect functionality
        self.connect_button = tk.Button(self.right_frame, text="Connect to DB", command=self.connect_to_db_handler, font=("Arial", 12))
        self.connect_button.pack(pady=10)

        # Right column login functionality
        self.login_label = tk.Label(self.right_frame, text="Enter Company Email:", bg="gray", fg="white", font=("Arial", 12))
        self.login_label.pack(pady=10)

        self.login_entry = tk.Entry(self.right_frame, font=("Arial", 12))
        self.login_entry.pack(pady=5)

        self.login_button = tk.Button(self.right_frame, text="Login", command=self.login, font=("Arial", 12))
        self.login_button.pack(pady=10)

        self.status_label = tk.Label(self.right_frame, text="Status: Disconnected", bg="gray", fg="white")
        self.status_label.pack(pady=20)

        self.db_connection = None

    def populate_left(self):
        for widget in self.left_frame.winfo_children():
            widget.destroy()

        elements = get_elements()
        for element in elements:
            button = tk.Button(
                self.left_frame, text=element["name"], command=lambda e=element: self.load_screen(e["name"])
            )
            button.pack(fill="x", pady=5)

    def load_screen(self, screen_name):
        for widget in self.middle_frame.winfo_children():
            widget.destroy()

        if screen_name == "Invoices":
            self.show_invoices()
        elif screen_name == "Register Company":
            self.register_company()
        elif screen_name == "Manage Company":
            self.manage_company()
        else:
            label = tk.Label(self.middle_frame, text=f"Screen: {screen_name}", font=("Arial", 18))
            label.pack(expand=True)

    def show_invoices(self):
        if not self.db_connection:
            label = tk.Label(self.middle_frame, text="Not connected to the database.", font=("Arial", 14), fg="red")
            label.pack(expand=True)
            return

        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT * FROM facility.faktury")
            rows = cursor.fetchall()

            columns = [desc[0] for desc in cursor.description]

            tree = ttk.Treeview(self.middle_frame, columns=columns, show="headings")
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=100)

            for row in rows:
                tree.insert("", "end", values=row)

            tree.pack(fill="both", expand=True)
        except Exception as e:
            label = tk.Label(self.middle_frame, text=f"Error retrieving invoices: {e}", font=("Arial", 14), fg="red")
            label.pack(expand=True)

    def manage_company(self):
        if not self.db_connection:
            label = tk.Label(self.middle_frame, text="Not connected to the database.", font=("Arial", 14), fg="red")
            label.pack(expand=True)
            return

        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT * FROM facility.firmy")
            rows = cursor.fetchall()

            columns = [desc[0] for desc in cursor.description]

            tree = ttk.Treeview(self.middle_frame, columns=columns, show="headings")
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=150)

            for row in rows:
                tree.insert("", "end", values=row)

            tree.pack(fill="both", expand=True)
        except Exception as e:
            label = tk.Label(self.middle_frame, text=f"Error retrieving companies: {e}", font=("Arial", 14), fg="red")
            label.pack(expand=True)

    def register_company(self):
        form_frame = tk.Frame(self.middle_frame)
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(form_frame, text="Company Name:", font=("Arial", 12)).grid(row=0, column=0, pady=5, sticky="e")
        company_name_entry = tk.Entry(form_frame, width=30, font=("Arial", 12))
        company_name_entry.grid(row=0, column=1, pady=5)

        tk.Label(form_frame, text="Country:", font=("Arial", 12)).grid(row=1, column=0, pady=5, sticky="e")
        country_entry = tk.Entry(form_frame, width=30, font=("Arial", 12))
        country_entry.grid(row=1, column=1, pady=5)

        tk.Label(form_frame, text="Address:", font=("Arial", 12)).grid(row=2, column=0, pady=5, sticky="e")
        address_entry = tk.Entry(form_frame, width=30, font=("Arial", 12))
        address_entry.grid(row=2, column=1, pady=5)

        tk.Label(form_frame, text="Email:", font=("Arial", 12)).grid(row=3, column=0, pady=5, sticky="e")
        email_entry = tk.Entry(form_frame, width=30, font=("Arial", 12))
        email_entry.grid(row=3, column=1, pady=5)

        tk.Label(form_frame, text="NIP (Numeric ID):", font=("Arial", 12)).grid(row=4, column=0, pady=5, sticky="e")
        nip_entry = tk.Entry(form_frame, width=30, font=("Arial", 12))
        nip_entry.grid(row=4, column=1, pady=5)

        def save_company():
            if not self.db_connection:
                tk.Label(form_frame, text="Not connected to the database.", font=("Arial", 12), fg="red").grid(row=7, columnspan=2)
                return

            name = company_name_entry.get().strip()
            country = country_entry.get().strip()
            address = address_entry.get().strip()
            email = email_entry.get().strip()
            nip = nip_entry.get().strip()

            if not name or not country or not address or not email or not nip:
                tk.Label(form_frame, text="All fields are required.", font=("Arial", 12), fg="red").grid(row=7, columnspan=2)
                return

            if not nip.isdigit() or len(nip) > 10:
                tk.Label(form_frame, text="NIP must be a numeric value up to 10 digits.", font=("Arial", 12), fg="red").grid(row=7, columnspan=2)
                return

            try:
                cursor = self.db_connection.cursor()
                cursor.execute(
                    "INSERT INTO facility.firmy (name, kraj, adres, mail, numeric_id) VALUES (%s, %s, %s, %s, %s)",
                    (name, country, address, email, nip)
                )
                self.db_connection.commit()
                tk.Label(form_frame, text="Company added successfully!", font=("Arial", 12), fg="green").grid(row=7, columnspan=2)
            except Exception as e:
                tk.Label(form_frame, text=f"Error: {e}", font=("Arial", 12), fg="red").grid(row=7, columnspan=2)

        tk.Button(form_frame, text="Save", command=save_company, font=("Arial", 12)).grid(row=6, columnspan=2, pady=10)

    def connect_to_db_handler(self):
        if self.db_connection:
            self.db_connection.close()

        self.db_connection = connect_to_db()
        if self.db_connection:
            self.status_label.config(text="Status: Connected", bg="green")
        else:
            self.status_label.config(text="Status: Connection Failed", bg="red")

    def login(self):
        global current_user
        email = self.login_entry.get().strip()

        if not self.db_connection:
            self.status_label.config(text="Status: Disconnected", bg="red")
            return

        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT name FROM facility.firmy WHERE mail = %s", (email,))
            result = cursor.fetchone()

            if result:
                current_user = result[0]
                self.status_label.config(text=f"Zalogowano jako {current_user}", bg="green")
            else:
                self.status_label.config(text="Invalid email", bg="red")
        except Exception as e:
            self.status_label.config(text=f"Error: {e}", bg="red")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()

    if ssh_tunnel:
        ssh_tunnel.stop()