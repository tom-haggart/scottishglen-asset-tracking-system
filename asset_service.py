# asset_service.py
# Collects hardware details from the machine being used.
# Validates asset and employee.

import platform
import socket
import subprocess
from models import HardwareDetails
from datetime import datetime

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

# macOS is for development only.
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

# macOS is for development path only.
def get_manufacturer():
    """Returns the manufacturer of this machine, or Unknown if it cannot be read."""
    try:
        if platform.system() == "Darwin":
            return "Apple"
        if platform.system() == "Windows":
            result = subprocess.run(["powershell", "-NoProfile", "-Command", "(Get-CimInstance Win32_ComputerSystem).Manufacturer"], capture_output=True, text=True, timeout=15)
            return result.stdout.strip() or "Unknown"
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

# 255 character limit matches the database (notes in schema.sql)
def validate_asset(employee_id, purchase_date_text, notes):
    """Checks the add-asset inputs and returns a list of error messages (empty if all valid)."""
    errors = []
    if employee_id is None:
        errors.append("Choose an employee")
    if purchase_date_text:
        try:
            datetime.strptime(purchase_date_text, "%Y-%m-%d")
        except ValueError:
            errors.append("Wrong format used. Correct format: YYYY-MM-DD")
    if notes and len(notes) > 255:
        errors.append("Note is too long. Character limit: 255")
    return errors

# Limits match the database (schema.sql)
def validate_employee(first_name, last_name, email, department_id):
    """Checks the add-employee inputs and returns a list of error messages (empty if all valid)."""
    errors = []
    first_name = first_name.strip()
    if not first_name:
        errors.append("Enter a first name")
    elif len(first_name) > 50:
        errors.append("First name is too long. Character limit: 50")
    last_name = last_name.strip()
    if not last_name:
        errors.append("Enter a last name")
    elif len(last_name) > 50:
        errors.append("Last name is too long. Character limit: 50")
    email = email.strip()
    if not email:
        errors.append("Enter an email")
    elif "@" not in email or "." not in email:
        errors.append("Email address is not valid")
    elif len(email) > 100:
        errors.append("Email is too long. Character limit: 100")
    if department_id is None:
        errors.append("Choose a department")
    return errors

# Quick manual test: only runs when this file is run directly. Checks validation.
if __name__ == "__main__":
    details = collect_hardware_details()
    print(details.system_name, details.asset_type, details.ip_address, details.model, details.manufacturer)
    print(validate_asset(1, None, None))
    print(validate_asset(None, "13/45/2026", "x" * 300))
    print(validate_employee("John", "Stewart", "John@example.com", 1))
    print(validate_employee("", "", "bad", None))