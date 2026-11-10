# models.py
# The data classes for the asset record app: what an employee, asset, hardware details, and department hold.
# They contain no database or screen code.

class Employee:
    """An employee who is responsible for an asset. All 5 details are required"""
    def __init__(self, first_name, last_name, email, department, employee_id):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.department = department
        self.employee_id = employee_id

class HardwareDetails:
    """The hardware details of the machine used to log assets.
    All 5 details are required"""
    def __init__(self, system_name, model, manufacturer, asset_type, ip_address):
        self.system_name = system_name
        self.model = model
        self.manufacturer = manufacturer
        self.asset_type = asset_type
        self.ip_address = ip_address

class Asset:
    """A piece of hardware linked to an employee.
    asset id, hardware details, and employee are required.
    purchase date and notes are optional"""
    def __init__(self, asset_id, hardware_details, employee, purchase_date=None, notes=None):
        self.asset_id = asset_id
        self.hardware_details = hardware_details
        self.employee = employee
        self.notes = notes
        self.purchase_date = purchase_date

class Department:
    """The department where an employee works.
    department_name is required."""
    def __init__(self, department_name):
        self.department_name = department_name

# Quick maual test of the models, using dummy data.
# Only runs when this file is run directly, not when it is imported.
if __name__ == "__main__":
    d = Department("Sales")
    e = Employee("Tom", "Haggart", "123.456@gmail.com", d, 6767)
    h = HardwareDetails("PC-01", "XPS 13", "Dell", "Laptop", "192.168.1.10")
    a = Asset(3445, h, e)
    print(a.hardware_details.model, a.employee.first_name, a.notes)

