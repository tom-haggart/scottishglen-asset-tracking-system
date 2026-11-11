# asset_service.py
# Collects hardware details from the machine being used.

import platform
import socket
from models import HardwareDetails

def collect_hardware_details():
    """Builds a HardwareDetails object from the machine this is running on.
    model, manufacturer and ip_address have placeholders."""
    system_name = platform.node()
    model = "Unknown"
    manufacturer = "Unknown"
    asset_type = platform.system()
    ip_address = "Unknown"
    return HardwareDetails(system_name, model, manufacturer, asset_type, ip_address)

# Quick manual test: only runs when this file is run directly.
if __name__ == "__main__":
    details = collect_hardware_details()
    print(details.system_name, details.asset_type)