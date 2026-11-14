# assets_tab.py
# The Assets tab: a table of assets with Add, Edit and Delete buttons.

import tkinter as tk
from tkinter import ttk, messagebox
from database import get_assets, delete_asset
from asset_dialog import open_asset_dialog

def build_assets_tab(parent):
    """Builds the Assets tab inside parent and returns it."""
    tab = ttk.Frame(parent)

    columns = ("asset_id", "system_name", "model", "asset_type", "ip_address","employee", "purchase_date", "notes")
    table = ttk.Treeview(tab, columns=columns, show="headings", selectmode="browse")
    table.heading("asset_id", text="ID")
    table.heading("system_name", text="System name")
    table.heading("model", text="Model")
    table.heading("asset_type", text="Type")
    table.heading("ip_address", text="IP address")
    table.heading("employee", text="Employee")
    table.heading("purchase_date", text="Purchase date")
    table.heading("notes", text="Notes")
    table.column("asset_id", width=50, anchor="center", stretch=False)
    table.pack(fill="both", expand=True, padx=10, pady=10)

    # Remembers which Asset each table row shows, so Edit and Delete know which is selected.
    assets_by_row = {}

    def refresh():
        """Reloads the table from the database."""
        table.delete(*table.get_children())
        assets_by_row.clear()
        for asset in get_assets():
            employee_name = f"{asset.employee.first_name} {asset.employee.last_name}"
            row_id = table.insert("", "end", values=(
                asset.asset_id,
                asset.hardware_details.system_name,
                asset.hardware_details.model,
                asset.hardware_details.asset_type,
                asset.hardware_details.ip_address,
                employee_name,
                asset.purchase_date or "",
                asset.notes or ""))
            assets_by_row[row_id] = asset

    def selected_asset():
        """Returns the Asset for the selected row, or None (with a message) if nothing is selected."""
        selection = table.selection()
        if not selection:
            messagebox.showinfo("Select an asset", "Click a row in the table first")
            return None
        return assets_by_row[selection[0]]
    
    def add():
        open_asset_dialog(tab.winfo_toplevel(), on_saved=refresh)

    def edit():
        asset = selected_asset()
        if asset is not None:
            open_asset_dialog(tab.winfo_toplevel(), asset, on_saved=refresh)

    def delete():
        asset = selected_asset()
        if asset is None:
            return
        if not messagebox.askyesno("Delete asset", f"Delete asset {asset.asset_id} ({asset.hardware_details.system_name})?"):
            return
        delete_asset(asset.asset_id)
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
    build_assets_tab(root).pack(fill="both", expand=True)
    root.mainloop()