import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import requests

DB = "jewelers.db"

# ---------------- DATABASE INIT ----------------
def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    # Companies
    c.execute("""
    CREATE TABLE IF NOT EXISTS companies(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        gst TEXT,
        address TEXT
    )
    """)

    # Purchases
    c.execute("""
    CREATE TABLE IF NOT EXISTS purchases(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        company TEXT,
        metal TEXT,
        weight REAL,
        rate REAL,
        total REAL
    )
    """)

    # Sales
    c.execute("""
    CREATE TABLE IF NOT EXISTS sales(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        customer TEXT,
        metal TEXT,
        weight REAL,
        rate REAL,
        making REAL,
        total REAL,
        paid REAL,
        balance REAL
    )
    """)

    # Orders
    c.execute("""
    CREATE TABLE IF NOT EXISTS orders(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        customer TEXT,
        ornament TEXT,
        weight REAL,
        advance REAL,
        balance REAL,
        status TEXT
    )
    """)

    # Karigar
    c.execute("""
    CREATE TABLE IF NOT EXISTS karigar(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        work_given REAL,
        work_received REAL,
        making_due REAL
    )
    """)

    # Gold Rates
    c.execute("""
    CREATE TABLE IF NOT EXISTS rates(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        gold22 REAL,
        gold24 REAL,
        silver REAL,
        updated_at TEXT
    )
    """)

    conn.commit()
    conn.close()

# ---------------- MAIN APP ----------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Londhe Jewelers ERP")
        self.geometry("900x600")

        tabs = ttk.Notebook(self)
        tabs.pack(fill="both", expand=True)

        self.rate_tab = ttk.Frame(tabs)
        self.sales_tab = ttk.Frame(tabs)
        self.purchase_tab = ttk.Frame(tabs)
        self.karigar_tab = ttk.Frame(tabs)

        tabs.add(self.rate_tab, text="Gold Rate")
        tabs.add(self.sales_tab, text="Sales")
        tabs.add(self.purchase_tab, text="Purchases")
        tabs.add(self.karigar_tab, text="Karigar")

        self.create_rate_tab()

    # ---------------- GOLD RATE TAB ----------------
    def create_rate_tab(self):
        frame = self.rate_tab

        tk.Label(frame, text="22K Gold Rate").pack()
        self.g22 = tk.Entry(frame)
        self.g22.pack()

        tk.Label(frame, text="24K Gold Rate").pack()
        self.g24 = tk.Entry(frame)
        self.g24.pack()

        tk.Label(frame, text="Silver Rate").pack()
        self.silver = tk.Entry(frame)
        self.silver.pack()

        tk.Button(frame, text="Save Locally", command=self.save_rate).pack(pady=10)
        tk.Button(frame, text="Update Online", command=self.update_online).pack()

    def save_rate(self):
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("INSERT INTO rates(gold22,gold24,silver,updated_at) VALUES(?,?,?,?)",
                  (self.g22.get(), self.g24.get(), self.silver.get(),
                   datetime.now().strftime("%d-%m-%Y %I:%M %p")))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Rate saved locally.")

    def update_online(self):
        try:
            import requests
            url = "http://127.0.0.1:5000/update"
            data = {
                "password": "LJ@2026",
                "gold22": self.g22.get(),
                "gold24": self.g24.get(),
                "silver": self.silver.get()
            }
            requests.post(url, data=data)
            messagebox.showinfo("Success", "Online rate updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
# ---------------- RUN ----------------
if __name__ == "__main__":
    init_db()
    app = App()
    app.mainloop()