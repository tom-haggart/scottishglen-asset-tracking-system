# add_asset_view.py
# The add-asset form
import tkinter as tk
from asset_service import collect_hardware_details
from tkinter import ttk
from database import get_employees

def build_form():
    """Builds and returns the add-asset window.
    The window contains: Hardware details shown automatically,
    plus the employee dropdown, purchase date box and notes box."""
    window = tk.Tk()
    window.title("Add Asset")
    hardware = collect_hardware_details()
    # The hardware section, shown read-only because it's collected automatically.
    tk.Label(window, text="Hardware details (collected automatically)").pack(pady=5)
    tk.Label(window, text=f"System name: {hardware.system_name}").pack()
    tk.Label(window, text=f"Model: {hardware.model}").pack()
    tk.Label(window, text=f"Manufacturer: {hardware.manufacturer}").pack()
    tk.Label(window, text=f"Type: {hardware.asset_type}").pack()
    tk.Label(window, text=f"IP address: {hardware.ip_address}").pack()

    # The employee dropdown.
    employees = get_employees()
    # A dictionary mapping the text shown in the dropdown to the employee's id
    employee_lookup = {}
    for employee in employees:
        label = f"{employee.first_name} {employee.last_name} ({employee.department.department_name})"
        employee_lookup[label] = employee.employee_id

    tk.Label(window, text="Employee").pack(pady=(10,0))
    employee_box = ttk.Combobox(window, values=list(employee_lookup.keys()), state="readonly")
    employee_box.pack()

    # The date input.
    tk.Label(window, text="Purchase date (YYYY-MM-DD, optional)").pack(pady=(10, 0))
    date_entry = tk.Entry(window)
    date_entry.pack()

    # The notes input.
    tk.Label(window, text="Notes (optional, max 255 characters)").pack(pady=(10, 0))
    notes_entry = tk.Entry(window, width=40)
    notes_entry.pack()

    return window