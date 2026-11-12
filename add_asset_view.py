# add_asset_view.py
# The add-asset form
import tkinter as tk
import sv_ttk
from asset_service import collect_hardware_details, validate_asset
from tkinter import ttk, messagebox
from database import get_employees, add_asset

def build_form():
    """Builds and returns the add-asset window.
    The window contains: Hardware details shown automatically,
    plus the employee dropdown, purchase date box, notes box and save button."""
    window = tk.Tk()
    window.title("Add Asset")
    hardware = collect_hardware_details()
    # The hardware section, shown read-only because it's collected automatically.
    ttk.Label(window, text="Hardware details (collected automatically)").pack(pady=5)
    ttk.Label(window, text=f"System name: {hardware.system_name}").pack()
    ttk.Label(window, text=f"Model: {hardware.model}").pack()
    ttk.Label(window, text=f"Manufacturer: {hardware.manufacturer}").pack()
    ttk.Label(window, text=f"Type: {hardware.asset_type}").pack()
    ttk.Label(window, text=f"IP address: {hardware.ip_address}").pack()

    # The employee dropdown.
    employees = get_employees()
    # A dictionary mapping the text shown in the dropdown to the employee's id
    employee_lookup = {}
    for employee in employees:
        label = f"{employee.first_name} {employee.last_name} ({employee.department.department_name})"
        employee_lookup[label] = employee.employee_id

    ttk.Label(window, text="Employee").pack(pady=(10,0))
    employee_box = ttk.Combobox(window, values=list(employee_lookup.keys()), state="readonly")
    employee_box.pack()

    # The date input.
    ttk.Label(window, text="Purchase date (YYYY-MM-DD, optional)").pack(pady=(10, 0))
    date_entry = ttk.Entry(window)
    date_entry.pack()

    # The notes input.
    ttk.Label(window, text="Notes (optional, max 255 characters)").pack(pady=(10, 0))
    notes_entry = ttk.Entry(window, width=40)
    notes_entry.pack()

    def save_asset():
        """Reads the form, validates it, and saves the asset."""
        # The dropdown only gives back the shown text, so look up the id.
        employee_id = employee_lookup.get(employee_box.get())
        date_text = date_entry.get().strip()
        notes_text = notes_entry.get().strip()

        errors = validate_asset(employee_id, date_text, notes_text)
        if errors:
            messagebox.showerror("Cannot save", "\n".join(errors))
            return

        # Blank boxes must go to the database as None, not ""
        purchase_date = date_text or None
        notes = notes_text or None
        asset_id = add_asset(hardware, employee_id, purchase_date, notes)
        messagebox.showinfo("Saved", f"Asset saved with ID {asset_id}")

    ttk.Button(window, text="Save", command=save_asset).pack(pady=15)

    # Applies sv-ttk theme (Modern Windows 11 theme) to the window.
    # Only restyles ttk widgets.
    sv_ttk.set_theme("light")

    return window