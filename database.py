# database.py
# Connects the app to the hosted databse.

import pyodbc
import config

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

# Quick manual test: connects and counts the departments (should print 5).
if __name__ == "__main__":
    with get_connection() as conn:
        row = conn.cursor().execute("SELECT COUNT(*) FROM department"). fetchone()
        print("Departments:", row[0])