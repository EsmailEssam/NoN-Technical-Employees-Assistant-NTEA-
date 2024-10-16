import sqlite3
import hashlib
import os
from dotenv import load_dotenv


# Load the Key token
_ = load_dotenv(override=True)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def authenticate_user(email, password):
    conn = sqlite3.connect('database/company.db')
    cur = conn.cursor()

    # Retrieve the password hash and salt for the given email
    cur.execute('''
        SELECT password_hash, salt, auth.employee_id FROM auth
        JOIN employees ON auth.employee_id = employees.employee_id
        WHERE email = ?
    ''', (email,))
    result = cur.fetchone()

    if result is None:
        return None, "User not found"

    stored_hash, salt, employee_id = result

    # Hash the provided password with the stored salt
    hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()

    # Check if the provided password is correct
    if hashed_password == stored_hash:
        return employee_id, "Authenticated"
    else:
        return None, "Invalid password"

