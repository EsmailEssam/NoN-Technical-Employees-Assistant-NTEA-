# Import the Libraries
from fastapi import FastAPI, Form, Depends, HTTPException, status
from fastapi.responses import FileResponse, StreamingResponse
from typing import List

# My Custom Functions
from helper.authentication import authenticate_employee
from helper.chatbot import query_llm
from helper.data import get_data

# Initialize an app
app = FastAPI(title="NTEA", debug=True)

# ---------------------------------------------- EndPoint for ChatBot ------------------------------------- #


@app.post("/chatbot", tags=["ChatBot"])
def chatbot(user_data: dict = Depends(get_data), user_question: str = Form(...)):

    # Call the custom Function
    response = query_llm(user_data, user_question)
    return f"ChatBot: {response}"


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
