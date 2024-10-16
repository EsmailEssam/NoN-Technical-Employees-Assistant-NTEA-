import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('database/company.db')

# Create a cursor object
cur = conn.cursor()

# Create Departments Table
cur.execute('''
CREATE TABLE IF NOT EXISTS departments (
    department_id INTEGER PRIMARY KEY AUTOINCREMENT,
    department_name TEXT UNIQUE NOT NULL
);
''')

# Create Positions Table
cur.execute('''
CREATE TABLE IF NOT EXISTS positions (
    position_id INTEGER PRIMARY KEY AUTOINCREMENT,
    position_name TEXT UNIQUE NOT NULL
);
''')

# Create Employees Table with foreign keys to departments and positions
cur.execute('''
CREATE TABLE IF NOT EXISTS employees (
    employee_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone_number TEXT,
    department_id INTEGER,
    position_id INTEGER,
    hire_date TEXT,
    status TEXT DEFAULT 'active',  -- 'active', 'inactive', 'terminated'
    FOREIGN KEY (department_id) REFERENCES departments(department_id),
    FOREIGN KEY (position_id) REFERENCES positions(position_id)
);
''')

# Create Salaries Table with timestamps for tracking changes
cur.execute('''
CREATE TABLE IF NOT EXISTS salaries (
    salary_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER,
    base_salary REAL,
    bonus REAL,
    currency TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);
''')

# Create Leaves Table with historical record-keeping for leave balance changes
cur.execute('''
CREATE TABLE IF NOT EXISTS leaves (
    leave_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER,
    annual_leave_balance REAL,
    sick_leave_balance REAL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);
''')

# Create Performance Table with composite key (employee_id, review_period)
cur.execute('''
CREATE TABLE IF NOT EXISTS performance (
    performance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER,
    rating REAL,
    review_period TEXT,
    last_review_date TEXT,
    UNIQUE (employee_id, review_period),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);
''')

# Create Auth Table with password salt for enhanced security
cur.execute('''
CREATE TABLE IF NOT EXISTS auth (
    auth_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER,
    password_hash TEXT,
    salt TEXT,
    last_login TEXT,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);
''')

# # Create indexes to improve performance on common query columns
cur.executescript('''
CREATE INDEX IF NOT EXISTS idx_employee_email ON employees(email);
CREATE INDEX IF NOT EXISTS idx_salary_employee_id ON salaries(employee_id);
CREATE INDEX IF NOT EXISTS idx_auth_employee_id ON auth(employee_id);
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database and tables created successfully.")
