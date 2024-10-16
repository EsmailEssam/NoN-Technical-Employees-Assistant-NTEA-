import os
import sqlite3
from openai import OpenAI
from dotenv import load_dotenv


# Load the Key token
_ = load_dotenv(override=True)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


def get_client_data(employee_id):
    conn = sqlite3.connect('database/company.db')
    cur = conn.cursor()

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

    cur.execute(query, (employee_id,))
    client_data = cur.fetchone()
    conn.close()

    # Return the data as a dictionary
    columns = ['employee_id', 'first_name', 'last_name', 'email', 'phone_number', 'department_name', 'position_name',
               'hire_date', 'status', 'base_salary', 'bonus', 'currency', 'salary_last_updated', 
               'annual_leave_balance', 'sick_leave_balance', 'leave_last_updated', 
               'performance_rating', 'review_period', 'last_review_date', 'last_login']
    
    return dict(zip(columns, client_data))

def generate_chat_response(client_data, user_input):
    # Create a context or prompt using the client's data
    context = [
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "system", 
            "content": f"""
            Employee ID: {client_data['employee_id']}
            Name: {client_data['first_name']} {client_data['last_name']}
            Department: {client_data['department_name']}
            Position: {client_data['position_name']}
            Base Salary: {client_data['base_salary']}
            Bonus: {client_data['bonus']}
            Hire Date: {client_data['hire_date']}
            Performance Rating: {client_data.get('performance_rating', 'N/A')}
            Leave Balance: {client_data.get('annual_leave_balance', 'N/A')} days
            Sick Leave Balance: {client_data.get('sick_leave_balance', 'N/A')} days
            Last Login: {client_data.get('last_login', 'N/A')}
            """
        },
        {"role": "user", "content": user_input}
    ]
    # Use the context and user input in the LLM prompt
    client = OpenAI(
        api_key=OPENAI_API_KEY,
    )
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=context
    )
    
    return response.choices[0].message.content