import os
import sqlite3
import hashlib
import pandas as pd


# Function to authenticate employee using email and password
def authenticate_employee(email, password):
    
    # Get database path
    DTABASE_PATH = 'database/employee_data.db'
    
    # Connect to the database
    conn = sqlite3.connect(DTABASE_PATH)
    cursor = conn.cursor()

    # Hash the input password
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    # Query to find the employee with matching email and password hash
    cursor.execute(
        "SELECT * FROM employees WHERE email=? AND password_hash=?",
        (email, password_hash),
    )
    
    # Fetch one employee from the result
    employee = cursor.fetchone()

    # Close the connecion with the database
    conn.close()

    # Check if there any user retrieved
    if employee:
        return True
    return False