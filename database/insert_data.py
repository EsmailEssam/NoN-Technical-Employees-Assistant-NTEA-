import sqlite3
from faker import Faker
import random
from datetime import datetime
import hashlib
import os

# Initialize Faker for generating fake data
fake = Faker()

# Connect to the SQLite database
conn = sqlite3.connect('database/company.db')
cur = conn.cursor()

# Example departments and positions
departments = ['HR', 'Engineering', 'Marketing', 'Sales', 'Finance', 'Support']
positions = ['Manager', 'Software Engineer', 'Sales Executive', 'Accountant', 'HR Specialist']

# Function to insert bulk fake employee data
def insert_fake_employees(num_employees=1000):
    employees = []
    
    # Generate fake employee data
    for _ in range(num_employees):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        phone_number = fake.phone_number()
        department_id = random.randint(1, len(departments))  # Assuming department IDs start from 1
        position_id = random.randint(1, len(positions))  # Assuming position IDs start from 1
        hire_date = fake.date_this_decade().strftime('%Y-%m-%d')
        status = random.choice(['active', 'inactive', 'terminated'])
        
        # Add generated employee data to the list
        employees.append((first_name, last_name, email, phone_number, department_id, position_id, hire_date, status))
    
    # Insert all generated employee data into the database
    cur.executemany('''
        INSERT OR IGNORE INTO employees (first_name, last_name, email, phone_number, department_id, position_id, hire_date, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    ''', employees)

    conn.commit()

# Function to insert example departments and positions into their respective tables
def insert_departments_positions():
    # Insert departments with INSERT OR IGNORE to avoid UNIQUE constraint violations
    cur.executemany("INSERT OR IGNORE INTO departments (department_name) VALUES (?);", [(dept,) for dept in departments])

    # Insert positions
    cur.executemany("INSERT OR IGNORE INTO positions (position_name) VALUES (?);", [(pos,) for pos in positions])
     
    conn.commit()

# Insert departments and positions before inserting employees
insert_departments_positions()

# Insert 1000 fake employees into the database
insert_fake_employees(1000)

# Close the database connection
conn.close()

print("1000 fake employees inserted successfully!")



# Connect to the SQLite database
conn = sqlite3.connect('database/company.db')
cur = conn.cursor()

# Function to create a secure password hash
def hash_password(password):
    # Generate a random salt
    salt = os.urandom(16).hex()  # Convert binary salt to a hexadecimal string
    # Hash the password with the salt
    password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    return password_hash, salt

# Function to insert a new user into the auth table
def insert_user_auth(employee_id, password):
    password_hash, salt = hash_password(password)
    last_login = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Insert the user authentication data into the auth table
    cur.execute('''
        INSERT INTO auth (employee_id, password_hash, salt, last_login)
        VALUES (?, ?, ?, ?);
    ''', (employee_id, password_hash, salt, last_login))
    
    conn.commit()
    print(f"User {employee_id} added to auth table.")

# Example usage:
# Insert a new user into the auth table with employee_id=1 and password="123"
insert_user_auth(employee_id=1, password="123")

# Close the connection
conn.close()
