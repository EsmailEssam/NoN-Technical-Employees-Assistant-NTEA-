import sqlite3
import hashlib
import pandas as pd
import os
from config import get_project_root


# PROJECT_PATH = get_project_root()
# DATABASE_FOLDER = 'database'
# DATABASE_NAME = 'employee_data.db'
# DTABASE_PATH = os.path.join(PROJECT_PATH, DATABASE_FOLDER, DATABASE_NAME)

DTABASE_PATH = 'database/employee_data.db'
conn = sqlite3.connect(DTABASE_PATH)
cursor = conn.cursor()
print(DTABASE_PATH)
conn.close()