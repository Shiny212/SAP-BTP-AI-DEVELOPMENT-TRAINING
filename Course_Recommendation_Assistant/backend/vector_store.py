import os
from dotenv import load_dotenv

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from course_data import courses

# Load environment variables
load_dotenv()

# Create LangChain Documents
documents = []

for course in courses:
    content = f"""
Course ID: {course['course_id']}
Course Name: {course['course_name']}
Skills Taught: {', '.join(course['skills_taught'])}
Experience Level: {course['experience_level']}
Duration: {course['duration']}
Prerequisites: {', '.join(course['prerequisites'])}
Description: {course['course_description']}
"""

    documents.append(
        Document(
            page_content=content,
            metadata={
                "course_id": course["course_id"],
                "course_name": course["course_name"],
                "experience_level": course["experience_level"],
                "duration": course["duration"]
            }
        )
    )

# Create Hugging Face Embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Create FAISS Vector Store
vector_store = FAISS.from_documents(
    documents,
    embeddings
)

# Save the Vector Store
vector_store.save_local("db")

print("✅ FAISS Vector Store Created Successfully!")