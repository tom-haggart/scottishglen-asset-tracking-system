# ScottishGlen Asset Tracking System

The application collects hardware details from the machine which becomes an asset and allows you to create an employee and link it to the asset. The application also allows you to edit and delete both an employee and an asset. The application was made with Python using tkinter for the window and a Microsoft SQL Server database.

## Requirements

- Windows
- Python 3.12
- ODBC Driver 17 for SQL Server
- The packages listed in requirements.txt

## Setup

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Open the .env file and fill in the database host, user, password and database name.

## Database

Run schema.sql in SQL Server Management Studio to create the tables.

## Running the app

```
python main.py
```

## Network note

When off campus the database requires you to pass the university firewall.

If you can't connect the application will show:

Database unavailable, Cannot reach the database. Check your network connection or the university firewall, then try again.

## Project layout

- models.py: The four classes (Employee, Asset, HardwareDetails, Department), no database or screen code. 

- database.py: Every SQL query; the only file that talks to the database.

- asset_service.py: Reads this computer's hardware, and checks the input before it's saved.

- asset_dialog.py and employee_dialog.py: The Add/Edit pop-up windows.

- assets_tab.py and employees_tab.py: The tables with the Add, Edit and Delete buttons.

- main_window.py and main.py: main_window builds the window with its two tabs; main.py just starts it.

## Testing

- seed_test_data.sql: Adds 10,000 test assets (all marked SEED), to reach the "10,000 records" in the performance requirements.

- measure_performance.py: Times adding, editing, deleting and loading assets, and checks every asset ID is unique.

- cleanup_test_data.sql: Removes the test assets afterwards.

WARNING THESE SCRIPTS ARE FOR THE TEST DATABASE!.