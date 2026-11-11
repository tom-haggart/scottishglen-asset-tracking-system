# database.py
# Connects the app to the hosted database.
import pyodbc
import config

from models import Department, Employee

def get_connection():
    """Returns a connection to the hosted SQL Server database."""
    connection_string = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        f"SERVER={config.DB_HOST};"
        f"DATABASE={config.DB_NAME};"
        f"UID={config.DB_USER};"
        f"PWD={config.DB_PASSWORD};"
    )
    return pyodbc.connect(connection_string)

# Fills the form's department dropdown.
def get_departments():
    """Returns every department in the database as a list of department objects."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT department_id, department_name FROM department ORDER BY department_name")
        rows = cursor.fetchall()
        departments = []
        for row in rows:
            departments.append(Department(row.department_name, row.department_id))
        return departments

def add_employee(first_name, last_name, email, department_id):
    """Adds an employee to the database and returns the new employee_id."""
    with get_connection() as conn:
        cursor = conn.cursor()
        # Uses ? placeholder values. The values are passed separately, so the database treats them as data not as SQL, which prevents SQL injection.
        cursor.execute(
            "INSERT INTO employee (first_name, last_name, email, department_id) OUTPUT INSERTED.employee_id "
            "VALUES (?, ?, ?, ?)",
            first_name, last_name, email, department_id)
        return cursor.fetchone()[0]

def get_employees():
    """Returns every employee as a list of Employee objects, each with their Department."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT e.employee_id, e.first_name, e.last_name, e.email, "
            "d.department_id, d.department_name "
            "FROM employee e JOIN department d ON e.department_id = d.department_id "
            "ORDER BY e.last_name, e.first_name")
        employees = []
        for row in cursor.fetchall():
            department = Department(row.department_name, row.department_id)
            employees.append(Employee(row.first_name, row.last_name, row.email, department, row.employee_id))
        return employees

# purchase_date and notes may be None. This will be fixed during validation. 
def add_asset(hardware, employee_id, purchase_date, notes):
    """Saves an asset and its hardware details in one transaction and returns the new asset_id."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO hardware_details (system_name, model, manufacturer, asset_type, ip_address) OUTPUT INSERTED.hardware_id "
            "VALUES (?, ?, ?, ?, ?)",
            hardware.system_name, hardware.model, hardware.manufacturer, hardware.asset_type, hardware.ip_address)
        hardware_id = cursor.fetchone()[0]
        cursor.execute(
            "INSERT INTO asset (hardware_id, employee_id, notes, purchase_date) OUTPUT INSERTED.asset_id "
            "VALUES (?, ?, ?, ?)",
            hardware_id, employee_id, notes, purchase_date)
        return cursor.fetchone()[0]

# Quick manual test: prints each department and each employee.
if __name__ == "__main__":
    #new_id = add_employee("Test", "Employee", "test.employee@example.com", 1)
    #print("Added employee with ID", new_id)
    for department in get_departments():
        print(department.department_id, department.department_name)

    for employee in get_employees():
        print(employee.first_name, employee.last_name, employee.department.department_name)