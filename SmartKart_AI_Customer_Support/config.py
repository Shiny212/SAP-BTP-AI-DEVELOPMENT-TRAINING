"""
config.py

Gemini Configuration
"""

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# ---------------------------------------
# Load Environment Variables
# ---------------------------------------

load_dotenv()

# ---------------------------------------
# Gemini Model
# ---------------------------------------

llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    temperature=0
)