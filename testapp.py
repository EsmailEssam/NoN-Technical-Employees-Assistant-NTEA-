from helper.authentication import authenticate_employee
from helper.data import get_data
from helper.chatbot4st import query_llm

def chat_with_llm(email, password):
    # Step 1: Authenticate the user
    employee_id, status = authenticate_employee(email, password)
    if not employee_id:
        print(status)
        return 

    # Step 2: Retrieve client data
    client_data = get_data(employee_id)
    
    
    query_llm(client_data)


# # Example usage:
chat_with_llm("monica00@example.net", "123")