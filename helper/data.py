import os
import sqlite3
import hashlib
import pandas as pd
from fastapi import HTTPException, status


from .authentication import authenticate_employee


# Function to get employee data
def get_data(email, password):

    # Check if the employee is authenticated
    is_authenticated = authenticate_employee(email, password)
    
    # Raise exeption if not authenticated
    if not is_authenticated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # get database path
    DTABASE_PATH = 'database/employee_data.db'
    
    # Connect to the database
    conn = sqlite3.connect(DTABASE_PATH)
    cursor = conn.cursor()
    
    # Hash the input password
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    # Query to find the employee with matching email and password hash
    query = f"SELECT * FROM employees WHERE email = '{email}' AND password_hash = '{password_hash}'"

    # Get the data in DataFrame 
    df = pd.read_sql(query, conn)

    # Close the connecion with the database
    conn.close()

    # Return the data in a dictionary
    return df.to_dict("records")