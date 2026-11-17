# employees_tab.py
# The Employees tab: a table of employees with Add, Edit and Delete buttons.

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

    def selected_employee():
        """Returns the Employee for the selected row, or None (with a message) if nothing is selected."""
        selection = table.selection()
        if not selection:
            messagebox.showinfo("Select an employee", "Click a row in the table first")
            return None
        return employees_by_row[selection[0]]

    def add():
        open_employee_dialog(tab.winfo_toplevel(), on_saved=refresh)

    def edit():
        employee = selected_employee()
        if employee is not None:
            open_employee_dialog(tab.winfo_toplevel(), employee, on_saved=refresh)

    def delete():
        employee = selected_employee()
        if employee is None:
            return
        if not messagebox.askyesno("Delete employee", f"Delete {employee.first_name} {employee.last_name}?"):
            return
        try:
            delete_employee(employee.employee_id)
        except ValueError as error:
            messagebox.showerror("Cannot delete", str(error))
            return
        refresh()

    buttons = ttk.Frame(tab)
    buttons.pack(pady=(0, 10))
    ttk.Button(buttons, text="Add", command=add).pack(side="left", padx=5)
    ttk.Button(buttons, text="Edit", command=edit).pack(side="left", padx=5)
    ttk.Button(buttons, text="Delete", command=delete).pack(side="left", padx=5)

    refresh()
    return tab

# Quick manual test: shows the tab in a small window.
if __name__ == "__main__":
    root = tk.Tk()
    build_employees_tab(root).pack(fill="both", expand=True)
    root.mainloop()