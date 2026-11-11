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

# Quick manual test: prints each department's ID and name.
if __name__ == "__main__":
    for department in get_departments():
        print(department.department_id, department.department_name)