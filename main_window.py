# main_window.py
# The main window: one window with an Assets tab and an Employee tab.
import tkinter as tk
from tkinter import ttk
import sv_ttk
from assets_tab import build_assets_tab
from employees_tab import build_employees_tab
import pyodbc
from tkinter import messagebox

DATABASE_MESSAGE = "Cannot reach the database. Check your network connection or the university firewall, then start the program again."

def open_main_window():
    """Builds and shows the main window."""
    root = tk.Tk()
    root.title("ScottishGlen Asset Tracking System")
    sv_ttk.set_theme("light")
    root.geometry("1100x500")
    root.minsize(800, 400)

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)
    try:  
        notebook.add(build_assets_tab(notebook), text="Assets")
        notebook.add(build_employees_tab(notebook), text="Employees")
    except pyodbc.Error:
        root.withdraw()
        messagebox.showerror("Database unavailable", DATABASE_MESSAGE)
        root.destroy()
        return

    root.mainloop()

if __name__ == "__main__":
    open_main_window()