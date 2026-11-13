# asset_dialog.py
# The add/edit asset window.
import tkinter as tk
from tkinter import ttk, messagebox
from asset_service import collect_hardware_details, validate_asset
from database import get_employees, add_asset, update_asset

def open_asset_dialog(parent, asset=None, on_saved=None):
    """Opens a window to add an asset (recording this computer), or to edit one if an Asset is given.
    on_saved is called after a successful save, so the caller can refresh its table."""
    dialog = tk.Toplevel(parent)
    dialog.title("Edit Asset" if asset else "Add Asset")
    dialog.transient(parent)
    dialog.grab_set()

    # Add mode records this computer. Edit mode shows the stored details, which are read-only.
    hardware = asset.hardware_details if asset else collect_hardware_details()

    details = [
        ("System name", hardware.system_name),
        ("Model", hardware.model),
        ("Manufacturer", hardware.manufacturer),
        ("Type", hardware.asset_type),
        ("IP address", hardware.ip_address),
    ]
    for row, (name, value) in enumerate(details):
        ttk.Label(dialog, text=name).grid(row=row, column=0, sticky="w", padx=10, pady=2)
        ttk.Label(dialog, text=value).grid(row=row, column=1, sticky="w", padx=10, pady=2)

    # The employee dropdown.
    employees = get_employees()
    # A dictionary mapping the text shown in the dropdown to the employee's id
    employee_lookup = {}
    for employee in employees:
        label = f"{employee.first_name} {employee.last_name} ({employee.department.department_name})"
        employee_lookup[label] = employee.employee_id

    ttk.Label(dialog, text="Employee").grid(row=5, column=0, sticky="w", padx=10, pady=5)
    employee_box = ttk.Combobox(dialog, values=list(employee_lookup.keys()), state="readonly", width=40)
    employee_box.grid(row=5, column=1, padx=10, pady=5)

    # The date input.
    ttk.Label(dialog, text="Purchase date (YYYY-MM-DD, optional)").grid(row=6, column=0, sticky="w", padx=10, pady=5)
    date_entry = ttk.Entry(dialog, width=40)
    date_entry.grid(row=6, column=1, padx=10, pady=5)

    # The notes input.
    ttk.Label(dialog, text="Notes (optional, max 255 characters)").grid(row=7, column=0, sticky="w", padx=10, pady=5)
    notes_entry = ttk.Entry(dialog, width=40)
    notes_entry.grid(row=7, column=1, padx=10, pady=5)

    ttk.Button(dialog, text="Cancel", command=dialog.destroy).grid(row=8, column=0, padx=10, pady=10)

# Quick manual test: opens the dialog in Add mode and in Edit mode with the first stored asset.
if __name__ == "__main__":
    from database import get_assets
    root = tk.Tk()
    ttk.Button(root, text="Add asset", command=lambda: open_asset_dialog(root)).pack(padx=40, pady=40)
    ttk.Button(root, text="Edit first asset", command=lambda: open_asset_dialog(root, get_assets()[0])).pack(padx=40, pady=(0, 40))
    root.mainloop()