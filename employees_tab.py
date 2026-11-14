# employees_tab.py
# The Employees tab: a table of employees (Add, Edit, Delete buttons come next).

import tkinter as tk
from tkinter import ttk, messagebox
from database import get_employees, delete_employee
from employee_dialog import open_employee_dialog

def build_employees_tab(parent):
    """Builds the Employees tab inside parent and returns it."""
    tab = ttk.Frame(parent)

    columns = ("first_name", "last_name", "email", "department")
    table = ttk.Treeview(tab, columns=columns, show="headings", selectmode="browse")
    table.heading("first_name", text="First name")
    table.heading("last_name", text="Last name")
    table.heading("email", text="Email")
    table.heading("department", text="Department")
    table.pack(fill="both", expand=True, padx=10, pady=10)

    # Remembers which Employee each table row shows, so Edit and Delete know who is selected.
    employees_by_row = {}

    def refresh():
        """Reloads the table from the database."""
        table.delete(*table.get_children())
        employees_by_row.clear()
        for employee in get_employees():
            row_id = table.insert("", "end", values=(employee.first_name, employee.last_name, employee.email, employee.department.department_name))
            employees_by_row[row_id] = employee

    refresh()
    return tab

# Quick manual test: shows the tab in a small window.
if __name__ == "__main__":
    root = tk.Tk()
    build_employees_tab(root).pack(fill="both", expand=True)
    root.mainloop()