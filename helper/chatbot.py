import time
from .config import client


# Looping to make it much more easier
all_messages = list()


# Function to integrate LLM like GPT
def query_llm(client_data):
    
    # Create system prompt
    system_message = f"""
        You are an assistant helping non-technical employees with their questions using the information provided.
        
        You will receive the data about the employee in a dictionary
        the variables of the each dictionary are:
            - Employee ID: {client_data['employee_id']}
            - Name: {client_data['first_name']} {client_data['last_name']}
            - Department: {client_data['department_name']}
            - Position: {client_data['position_name']}
            - Base Salary: {client_data['base_salary']}
            - Bonus: {client_data['bonus']}
            - Hire Date: {client_data['hire_date']}
            - Performance Rating: {client_data.get('performance_rating', 'N/A')}
            - Review Period: {client_data.get('review_period', 'N/A')}
            - Last Review Date: {client_data.get('last_review_date', 'N/A')}
            - Leave Balance: {client_data.get('annual_leave_balance', 'N/A')} days
            - Sick Leave Balance: {client_data.get('sick_leave_balance', 'N/A')} days
            - Last Login: {client_data.get('last_login', 'N/A')}
        
        You are NOT ALLOWED to answer any question that not related to the information provided.
        """
    all_messages.append({"role": "system", "content": system_message})

    # Looping while true
    while True:
        
        user_question = input("You: ")

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
            user_prompt = f"Question: {user_question}"

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