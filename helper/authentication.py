import sqlite3
import hashlib


# Function to authenticate employee using email and password
def authenticate_employee(email, password):
    
    # Get database path
    DTABASE_PATH = 'database/company.db'
    
    # Connect to the database
    conn = sqlite3.connect(DTABASE_PATH)
    cursor = conn.cursor()

    # Retrieve the password hash and salt for the given email
    cursor.execute('''
        SELECT password_hash, salt, auth.employee_id FROM auth
        JOIN employees ON auth.employee_id = employees.employee_id
        WHERE email = ?
    ''', (email,))
    result = cursor.fetchone()

    if result is None:
        return None, "User not found"

    stored_hash, salt, employee_id = result

    # Hash the provided password with the stored salt
    hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()
    
    # Close the connecion with the database
    conn.close()

    # Check if the provided password is correct
    if hashed_password == stored_hash:
        return employee_id, "Authenticated"
    else:
        return None, "Invalid password"


# # Example usage:
# email = 'monica00@example.net', 
# password = '123'
# print(authenticate_employee(email, password))

# id, state = authenticate_employee(email, password)

# print(id, state)