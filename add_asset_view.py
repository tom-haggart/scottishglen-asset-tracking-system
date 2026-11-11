# add_asset_view.py
# The add-asset form
import tkinter as tk
from asset_service import collect_hardware_details

def build_form():
    """Builds and returns the add-asset window."""
    window = tk.Tk()
    window.title("Add Asset")
    hardware = collect_hardware_details()
    tk.Label(window, text="Hardware details (collected automatically)").pack(pady=5)
    tk.Label(window, text=f"System name: {hardware.system_name}").pack()
    tk.Label(window, text=f"Model: {hardware.model}").pack()
    tk.Label(window, text=f"Manufacturer: {hardware.manufacturer}").pack()
    tk.Label(window, text=f"Type: {hardware.asset_type}").pack()
    tk.Label(window, text=f"IP address: {hardware.ip_address}").pack()
    return window