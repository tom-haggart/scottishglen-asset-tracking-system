class Employee:
    def __init__(self, first_name, last_name, email, department):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.department = department

class HardwareDetails:
    def __init__(self, system_name, model, manufacturer, asset_type, ip_address):
        self.system_name = system_name
        self.model = model
        self.manufacturer = manufacturer
        self.asset_type = asset_type
        self.ip_address = ip_address

class Asset:
    def __init__(self, asset_id, hardware_details, employee, purchase_date=None, notes=None):
        self.asset_id = asset_id
        self.hardware_details = hardware_details
        self.employee = employee
        self.notes = notes
        self.purchase_date = purchase_date

if __name__== "__main__":
    e = Employee("Tom", "Haggart", "123.456@gmail.com", "sales")
    h = HardwareDetails("PC-01", "XPS 13", "Dell", "Laptop", "192.168.1.10")
    a = Asset("A001", h, e)
    print(a.hardware_details.model, a.employee.first_name, a.notes)