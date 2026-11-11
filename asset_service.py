# asset_service.py
# Collects hardware details from the machine being used.

import platform
import socket
from models import HardwareDetails

# This approach was suggested by an AI assistant (Claude).
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

def collect_hardware_details():
    """Builds a HardwareDetails object from the machine this is running on.
    model and manufacturer have placeholders."""
    system_name = platform.node()
    model = "Unknown"
    manufacturer = "Unknown"
    asset_type = platform.system()
    ip_address = get_ip_address()
    return HardwareDetails(system_name, model, manufacturer, asset_type, ip_address)

# Quick manual test: only runs when this file is run directly.
if __name__ == "__main__":
    details = collect_hardware_details()
    print(details.system_name, details.asset_type, details.ip_address)