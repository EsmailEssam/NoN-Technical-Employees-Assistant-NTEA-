import os
from openai import OpenAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv


# Load the Key token
_ = load_dotenv(override=True)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# OpenAI Client
client = OpenAI(api_key=OPENAI_API_KEY)

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004",
                                            google_api_key =GEMINI_API_KEY )