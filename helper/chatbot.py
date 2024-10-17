import os
import time
from openai import OpenAI
from .config import client


# Looping to make it much more easier
all_messages = list()

# Create system prompt
system_message = """
    You are an assistant helping non-technical employees with their questions using the information provided.
    You are NOT ALLOWED to answer any question that not related to the information provided.
    
    You will receive the data about the employee in a list of dictionary
    the variables of the each dictionary are:
        employee_id: Unique identifier for each employee
        first_name: Employee's first name
        last_name: Employee's last name
        email: Employee's email (used for authentication)
        phone_number: Employee's contact number
        department: Employee's department
        position: Job title or position
        hire_date: Date when the employee was hired
        base_salary: Employee's base salary
        bonus: Most recent bonus amount
        currency: Currency of the salary
        annual_leave_balance: Number of annual leave days remaining
        sick_leave_balance: Number of sick leave days remaining
        performance_rating: Latest performance rating (e.g., 4.5)
        review_period: Period of the last review (e.g., Q1, 2024)
        last_review_date: Date of the last performance review
        password_hash: Hashed password for secure authentication
        last_login: Date and time of the last login
    """
all_messages.append({"role": "system", "content": system_message})


# Function to integrate LLM like GPT
def query_llm(employee_data, user_question):

    # Looping while true
    while True:

        # If the user wants to exit the chatbot -> break
        if user_question.lower() in ["quit", "exit", "ex", "out", "escape"]:
            time.sleep(2)  # wait 2 seconds

            # If the user exit the chatbot, Clear it.
            all_messages.clear()
            return {"message": "Thanks for using my ChatBot"}

        # If the user doesn't write any thing -> Continue
        elif user_question.lower() == "":
            return {"message": "No input detected. Please enter a prompt."}

        else:
            # Format the employee data and question for the LLM
            user_prompt = f"""
            Employee Information: {employee_data}
            
            Question: {user_question}
            """

            # append the question of user to message as a user roke
            all_messages.append({"role": "user", "content": user_prompt})

            # model
            each_response = client.chat.completions.create(
                model="gpt-4o-mini", messages=all_messages
            )

            each_response = each_response.choices[0].message.content

            # We must append this respond to the messages
            all_messages.append({"role": "assistant", "content": each_response})

            return each_response
