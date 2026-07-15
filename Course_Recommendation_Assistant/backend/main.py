from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from rag_engine import recommend_course
from tools import calculate_total_learning_hours

# --------------------------------------------
# FastAPI App
# --------------------------------------------

app = FastAPI(
    title="Course Recommendation API",
    description="RAG-based Course Recommendation Assistant using LangChain and Gemini",
    version="1.0.0"
)

# --------------------------------------------
# Enable CORS
# --------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # For development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------
# Request Model
# --------------------------------------------

class QuestionRequest(BaseModel):
    question: str

# --------------------------------------------
# Root Endpoint
# --------------------------------------------

@app.get("/")
def home():
    return {
        "message": "Course Recommendation API is Running 🚀"
    }

# --------------------------------------------
# Recommendation Endpoint
# --------------------------------------------

@app.post("/recommend")
def recommend(request: QuestionRequest):

    try:

        response = recommend_course(request.question)

        durations = []

        for course in response["source_metadata"]:
            durations.append(course["duration"])

        total_hours = calculate_total_learning_hours.invoke(
            {
                "durations": durations
            }
        )

        response["total_learning_hours"] = total_hours

        return response

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )