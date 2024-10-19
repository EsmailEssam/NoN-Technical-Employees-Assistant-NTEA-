# Import the Libraries
from fastapi import FastAPI, Form, Depends, HTTPException, status
from fastapi.responses import FileResponse, StreamingResponse
from typing import List

# My Custom Functions
from helper.authentication import authenticate_employee
from helper.chatbot4api import query_llm
from helper.data import get_data

# Initialize an app
app = FastAPI(title="NTEA", debug=True)

# ---------------------------------------------- EndPoint for ChatBot ------------------------------------- #

def prepare(email, password):
    user_id, user_status = authenticate_employee(email, password)
    
    if not user_id:
        print(user_status)
        return
    
    user_data = get_data(user_id)
    
    return user_data


@app.post("/chatbot", tags=["ChatBot"])
def chatbot(user_data: dict = Depends(prepare), user_question: str = Form(...)):

    # user_id, user_status =  auth_data
    # print(auth_data)
    # user_data = get_data(user_id)
    
    # Call the custom Function
    query_llm(user_data, user_question)




# Authentication route to simulate login
@app.post("/login")
def login(email: str = Form(...), password: str = Form(...)):
    if authenticate_employee(email, password):
        return {"message": "Login successful!"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
