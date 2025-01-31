import streamlit as st
from helper.chatbot import query_llm
from helper.authentication import authenticate_employee
from helper.data import get_data

def chat_interface(user_data=None, guest_mode=None):
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    query_llm(user_data, guest_mode=guest_mode)

def main():
    st.title("Employees Assistant")

    # Check if user is logged in or accessing as guest
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'guest_mode' not in st.session_state:
        st.session_state.guest_mode = False

    if not st.session_state.logged_in and not st.session_state.guest_mode:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        # Create columns for the buttons
        col1, col2 = st.columns(2)

        # Place buttons in each column
        with col1:
            if st.button("Login", use_container_width=True):
                auth_result = authenticate_employee(email, password)
                if auth_result == 'User not found':
                    st.error('User not found')
                elif auth_result:
                    st.session_state.logged_in = True
                    st.session_state.ID = auth_result
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid credentials")

        with col2:
            # Add a guest mode button
            if st.button("Continue as Guest", use_container_width=True):
                st.session_state.guest_mode = True
                st.rerun()

    else:
        user_data = None
        if st.session_state.guest_mode:
            mode = 'guest'
            # Use default or limited data for guest users
            user_data = {"role": "guest", "content": "Welcome, Guest!"}
        else:
            user_data = get_data(st.session_state.ID)

            if user_data is None:
                st.error("Failed to retrieve user data. Please try logging in again.")
                st.session_state.logged_in = False
                st.rerun()

        chat_interface(user_data, guest_mode=st.session_state.guest_mode)

if __name__ == "__main__":
    main()

# # Example usage:
# Email: paulamanda@example.com
# PassWord: 123