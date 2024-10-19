import streamlit as st
from helper.authentication import authenticate_employee
from helper.data import get_data
from helper.chatbot4st import query_llm

# Streamlit app
def main():
    st.title("Chatbot App with Login")

    # Session state for tracking login and chat history
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # If not logged in, show login form
    if not st.session_state.logged_in:
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if authenticate_employee(username, password):
                st.session_state.logged_in = True
                st.success("Login successful!")
            else:
                st.error("Invalid credentials. Try again.")
    else:
        st.subheader("Chat with the Assistant")
        
        # Display the chat history
        if st.session_state.chat_history:
            for chat in st.session_state.chat_history:
                st.write(f"**You:** {chat['user']}")
                st.write(f"**Assistant:** {chat['bot']}")
        
        # Get user input
        user_input = st.text_input("Your message")
        if st.button("Send"):
            if user_input:
                # Generate a response using the chatbot
                bot_response = query_llm(user_input)
                
                # Save the chat to the session state
                st.session_state.chat_history.append({"user": user_input, "bot": bot_response})
                
                # Display the updated chat history
                st.write(f"**You:** {user_input}")
                st.write(f"**Assistant:** {bot_response}")
                
        # Logout button
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.chat_history = []

# Run the app
if __name__ == "__main__":
    main()