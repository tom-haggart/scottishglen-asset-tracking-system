# asset_dialog.py
# The add/edit asset window.
import tkinter as tk
from tkinter import ttk, messagebox
from asset_service import collect_hardware_details, validate_asset
from database import get_employees, add_asset, update_asset

def open_asset_dialog(parent, asset=None, on_saved=None):
    """Opens a window to add an asset (recording this computer), or to edit one if an Asset is given.
    on_saved is called after a successful save, so the caller can refresh its table."""
    # Add mode records this computer. Edit mode shows the stored details, which are read-only.
    hardware = asset.hardware_details if asset else collect_hardware_details()
    # Fetch what can fail (hardware, employees) before opening the window, so a database error leaves no half-built dialog.
    employees = get_employees()

    dialog = tk.Toplevel(parent)
    dialog.title("Edit Asset" if asset else "Add Asset")
    dialog.transient(parent)
    dialog.grab_set()

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

    # Shows how many of the 255 allowed characters have been used.
    notes_count = ttk.Label(dialog, text="0 / 255")
    notes_count.grid(row=7, column=2, padx=(0, 10))

    def update_count(event=None):
        notes_count.config(text=f"{len(notes_entry.get())} / 255")

    notes_entry.bind("<KeyRelease>", update_count)

    ttk.Button(dialog, text="Cancel", command=dialog.destroy).grid(row=8, column=0, padx=10, pady=10)

    # Edit mode: start with the asset's current employee, date and notes.
    if asset is not None:
        employee_box.set(f"{asset.employee.first_name} {asset.employee.last_name} ({asset.employee.department.department_name})")
        if asset.purchase_date is not None:
            date_entry.insert(0, str(asset.purchase_date))
        if asset.notes is not None:
            notes_entry.insert(0, asset.notes)
            update_count()

    def save():
        """Validates the inputs, then adds a new asset or updates the one being edited."""
        employee_id = employee_lookup.get(employee_box.get())
        date_text = date_entry.get().strip()
        notes_text = notes_entry.get().strip()

        errors = validate_asset(employee_id, date_text, notes_text)
        # Stays open on errors, so the user keeps what they typed.
        if errors:
            messagebox.showerror("Cannot save", "\n".join(errors))
            return

        # Blank boxes must go to the database as None not "".
        purchase_date = date_text or None
        notes = notes_text or None
        if asset is None:
            add_asset(hardware, employee_id, purchase_date, notes)
        else:
            update_asset(asset.asset_id, employee_id, purchase_date, notes)

        if on_saved is not None:
            on_saved()
        dialog.destroy()

    ttk.Button(dialog, text="Save", command=save).grid(row=8, column=1, sticky="e", padx=10, pady=10)

    # NFR 5: instructions stay visible while the user types.
    instructions = "Choose an employee (required). The date and notes are optional. " \
                   "Click Save to keep your changes, or Cancel to leave without saving."
    ttk.Label(dialog, text=instructions, wraplength=450, justify="left").grid(row=9, column=0, columnspan=2, sticky="w", padx=10, pady=(0,10))

# Quick manual test: opens the dialog in Add mode and in Edit mode with the first stored asset.
if __name__ == "__main__":
    from database import get_assets
    root = tk.Tk()
    ttk.Button(root, text="Add asset", command=lambda: open_asset_dialog(root)).pack(padx=40, pady=40)
    ttk.Button(root, text="Edit first asset", command=lambda: open_asset_dialog(root, get_assets()[0])).pack(padx=40, pady=(0, 40))
    root.mainloop()