# asset_service.py
# Collects hardware details from the machine being used.

import platform
import socket
import subprocess
from models import HardwareDetails

# The approach used for get_ip_address was suggested by an AI assistant (Claude).
# This follows the approach in https://docs.python.org/3/library/socket.html.
def get_ip_address():
    """Returns the ip address of the machine, or Unknown if it cannot be read."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80)) # Connecting a UDP socket sends no data and only makes the system choose your local address.
            ip = s.getsockname()[0]
        return ip
    except OSError:
        return "Unknown"

def get_model():
    """Returns the model of this machine, or Unknown if it cannot be read."""
    try:
        if platform.system() == "Darwin":
            result = subprocess.run(["sysctl", "-n", "hw.model"], capture_output=True, text=True, timeout=5)
            return result.stdout.strip() or "Unknown"
        if platform.system() == "Windows":
            result = subprocess.run(["powershell", "-NoProfile", "-Command", "(Get-CimInstance Win32_ComputerSystem).Model"], capture_output=True, text=True, timeout=15)
            return result.stdout.strip() or "Unknown"
        return "Unknown"
    except Exception:
        return "Unknown"

# macOS is for development path only 
def get_manufacturer():
    """Returns the manufacturer of this machine, or Unknown if it cannot be read."""
    try:
        if platform.system() == "Darwin":
            return "Apple"
        return "Unknown"
    except Exception:
        return "Unknown"

def collect_hardware_details():
    """Builds a HardwareDetails object from the machine this is running on."""
    system_name = platform.node()
    model = get_model()
    manufacturer = get_manufacturer()
    asset_type = platform.system()
    ip_address = get_ip_address()
    return HardwareDetails(system_name, model, manufacturer, asset_type, ip_address)

# Quick manual test: only runs when this file is run directly.
if __name__ == "__main__":
    details = collect_hardware_details()
    print(details.system_name, details.asset_type, details.ip_address, details.model, details.manufacturer)