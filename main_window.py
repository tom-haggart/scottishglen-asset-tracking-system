# main_window.py
# The main window: one window with an Assets tab and an Employees tab.
import sys
import tkinter as tk
from tkinter import ttk, messagebox

import pyodbc
import sv_ttk

from assets_tab import build_assets_tab
from employees_tab import build_employees_tab

DATABASE_MESSAGE = "Cannot reach the database. Check your network connection or the university firewall, then start the program again."

def show_error(error_type, error_value, error_traceback):
    """Called by tkinter when a button click raises an error. Database errors get a friendly message."""
    if issubclass(error_type, pyodbc.Error):
        messagebox.showerror("Database unavailable", "Cannot reach the database. Check your network connection or the university firewall, then try again.")
    else:
        sys.__excepthook__(error_type, error_value, error_traceback)

def open_main_window():
    """Builds and shows the main window."""
    root = tk.Tk()
    root.report_callback_exception = show_error
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