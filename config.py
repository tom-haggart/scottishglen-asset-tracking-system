# config.py
# Reads the database settings from the .env file so the password is never stored in code.
import os
from dotenv import load_dotenv

# Load the settings from the .env file into the program.
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Stop with a clear message if a setting is missing, instead of failing later with a confusing database error.
if None in (DB_HOST, DB_USER, DB_PASSWORD, DB_NAME):
    raise RuntimeError("Database settings are missing. Please copy .env.example to .env and fill it in.")