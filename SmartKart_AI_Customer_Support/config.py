"""
config.py

Loads environment variables and initializes
the Gemini Language Model.
"""

from dotenv import load_dotenv
import os

from langchain_google_genai import ChatGoogleGenerativeAI

# --------------------------------------------------
# Load Environment Variables
# --------------------------------------------------

load_dotenv()

# --------------------------------------------------
# Read API Key
# --------------------------------------------------

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY not found in the .env file."
    )

# --------------------------------------------------
# Initialize Gemini Model
# --------------------------------------------------

llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    temperature=0,
    google_api_key=GOOGLE_API_KEY,
)