# employee_dialog.py
# The add/edit employee window.
import tkinter as tk
from tkinter import ttk, messagebox
from database import get_departments, add_employee, update_employee
from asset_service import validate_employee

def open_employee_dialog(parent, employee=None, on_saved=None):
    """Opens a window to add an employee, or to edit one if an Employee is given.
    on_saved is called after a successful save, so the caller can refresh its table."""
    dialog = tk.Toplevel(parent)
    dialog.title("Edit Employee" if employee else "Add Employee")
    # Keeps the dialog on top of the main window and blocks it until this one is closed.
    dialog.transient(parent)
    dialog.grab_set()

    # Maps the department name shown in the dropdown to its id, like the employee lookup on the asset form.
    department_lookup = {}
    for department in get_departments():
        department_lookup[department.department_name] = department.department_id

    ttk.Label(dialog, text="First name").grid(row=0, column=0, sticky="w", padx=10, pady=5)
    first_name_entry = ttk.Entry(dialog, width=30)
    first_name_entry.grid(row=0, column=1, padx=10, pady=5)
    ttk.Label(dialog, text="Last name").grid(row=1, column=0, sticky="w", padx=10, pady=5)
    last_name_entry = ttk.Entry(dialog, width=30)
    last_name_entry.grid(row=1, column=1, padx=10, pady=5)
    ttk.Label(dialog, text="Email").grid(row=2, column=0, sticky="w", padx=10, pady=5)
    email_entry = ttk.Entry(dialog, width=30)
    email_entry.grid(row=2, column=1, padx=10, pady=5)
    ttk.Label(dialog, text="Department").grid(row=3, column=0, sticky="w", padx=10, pady=5)
    department_box = ttk.Combobox(dialog, values=list(department_lookup.keys()), state="readonly", width=27)
    department_box.grid(row=3, column=1, padx=10, pady=5)
    ttk.Button(dialog, text="Cancel", command=dialog.destroy).grid(row=4, column=0, padx=10, pady=10)

    # Edit mode: start with employee's current details.
    if employee is not None:
        first_name_entry.insert(0, employee.first_name)
        last_name_entry.insert(0, employee.last_name)
        email_entry.insert(0, employee.email)
        department_box.set(employee.department.department_name)

# Quick manual test: opens the dialog from a small test window.
if __name__ == "__main__":
    root = tk.Tk()
    ttk.Button(root, text="Add employee", command=lambda: open_employee_dialog(root)).pack(padx=40, pady=40)

    from models import Employee, Department
    sample = Employee("John", "Stewart", "john@example.com", Department("Finance", 5), 99)
    ttk.Button(root, text="Edit sample employee", command=lambda: open_employee_dialog(root, sample)).pack(padx=40, pady=(0, 40))
    root.mainloop()