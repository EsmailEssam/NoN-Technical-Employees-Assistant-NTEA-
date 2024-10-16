from authentication import authenticate_user
from llm import generate_chat_response, get_client_data


def chat_with_llm(email, password):
    # Step 1: Authenticate the user
    employee_id, status = authenticate_user(email, password)
    if not employee_id:
        print(status)
        return
    
    # Step 2: Retrieve client data
    client_data = get_client_data(employee_id)
    
    # Step 3: Begin chatting with the LLM
    print(f"Welcome, {client_data['first_name']} {client_data['last_name']}!\n")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            break
        
        # Step 4: Generate LLM response using the client data and user input
        response = generate_chat_response(client_data, user_input)
        print(f"AI: {response}\n")

# # Example usage:
# email = input("Email: ")
# password = input("Password: ")
# chat_with_llm(email, password)
chat_with_llm('monica00@example.net', '123')
