import sqlite3


# Function to get employee data
def get_data(employee_id):
    # get database path
    DTABASE_PATH = 'database/company.db'
    
    # Connect to the database
    conn = sqlite3.connect(DTABASE_PATH)
    cursor = conn.cursor()
    
    query = '''
    SELECT 
        e.employee_id,
        e.first_name,
        e.last_name,
        e.email,
        e.phone_number,
        d.department_name,
        p.position_name,
        e.hire_date,
        e.status,
        s.base_salary,
        s.bonus,
        s.currency,
        s.created_at AS salary_last_updated,
        l.annual_leave_balance,
        l.sick_leave_balance,
        l.updated_at AS leave_last_updated,
        perf.rating AS performance_rating,
        perf.review_period,
        perf.last_review_date,
        a.last_login
    FROM 
        employees e
    JOIN 
        departments d ON e.department_id = d.department_id
    JOIN 
        positions p ON e.position_id = p.position_id
    LEFT JOIN 
        salaries s ON e.employee_id = s.employee_id
    LEFT JOIN 
        leaves l ON e.employee_id = l.employee_id
    LEFT JOIN 
        performance perf ON e.employee_id = perf.employee_id
    LEFT JOIN 
        auth a ON e.employee_id = a.employee_id
    WHERE 
        e.employee_id = ?;
    '''

    cursor.execute(query, (employee_id,))
    client_data = cursor.fetchone()
    conn.close()

    # Return the data as a dictionary
    columns = ['employee_id', 'first_name', 'last_name', 'email', 'phone_number', 'department_name', 'position_name',
               'hire_date', 'status', 'base_salary', 'bonus', 'currency', 'salary_last_updated', 
               'annual_leave_balance', 'sick_leave_balance', 'leave_last_updated', 
               'performance_rating', 'review_period', 'last_review_date', 'last_login']
    
    # Close the connecion with the database
    conn.close()
    
    return dict(zip(columns, client_data))



# # Example usage:
# print(get_data(employee_id=1))