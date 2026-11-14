# main_window.py
# The main window: one window with an Assets tab and an Employee tab.
import tkinter as tk
from tkinter import ttk
import sv_ttk
from assets_tab import build_assets_tab
from employees_tab import build_employees_tab

def open_main_window():
    """Builds and shows the main window."""
    root = tk.Tk()
    root.title("ScottishGlen Asset Tracking System")
    sv_ttk.set_theme("light")

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)
    notebook.add(build_assets_tab(notebook), text="Assets")
    notebook.add(build_employees_tab(notebook), text="Employees")

    root.mainloop()

if __name__ == "__main__":
    open_main_window()