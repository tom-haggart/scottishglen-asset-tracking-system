# database.py
# Connects the app to the hosted database.
import pyodbc
import config

from models import Department

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

# Quick manual test: adds one test employee, then prints each department's ID and name. The test now adds the employee first.
if __name__ == "__main__":
    new_id = add_employee("Test", "Employee", "test.employee@example.com", 1)
    print("Added employee with ID", new_id)
    for department in get_departments():
        print(department.department_id, department.department_name)