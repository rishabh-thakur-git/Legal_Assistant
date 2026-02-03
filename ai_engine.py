import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

def load_model():
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    return genai.GenerativeModel("gemini-pro")

def generate_response(model, prompt: str) -> str:
    response = model.generate_content(prompt)
    return response.text

