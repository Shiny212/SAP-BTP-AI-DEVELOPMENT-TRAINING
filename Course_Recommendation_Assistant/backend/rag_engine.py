from dotenv import load_dotenv

load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from models import CourseRecommendation

# -----------------------------
# Load Embedding Model
# -----------------------------

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# -----------------------------
# Load FAISS Database
# -----------------------------

vector_store = FAISS.load_local(
    "db",
    embeddings,
    allow_dangerous_deserialization=True
)

retriever = vector_store.as_retriever(
    search_kwargs={"k": 5}
)

# -----------------------------
# Gemini Model
# -----------------------------

llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    temperature=0.2
)

# -----------------------------
# Conversation History
# -----------------------------

conversation_history = []

# -----------------------------
# Output Parser
# -----------------------------

parser = JsonOutputParser(
    pydantic_object=CourseRecommendation
)

# -----------------------------
# Prompt
# -----------------------------

prompt = ChatPromptTemplate.from_template("""
You are an expert SAP Business AI Learning Advisor.

Answer ONLY using the supplied course documents.

Conversation History:
{history}

Course Documents:
{context}

User Question:
{question}

Instructions:

1. Recommend one or more suitable courses.
2. Explain why they were selected.
3. Mention prerequisites.
4. Suggest the correct learning sequence.
5. Give a confidence score between 0 and 1.
6. Use the supplied documents only.
7. Do not invent courses.

Return ONLY valid JSON.

{format_instructions}
""")

# -----------------------------
# Main Function
# -----------------------------

def recommend_course(question: str):

    docs = retriever.invoke(question)

    context = "\n\n".join(
        doc.page_content for doc in docs
    )

    source_metadata = [
        doc.metadata
        for doc in docs
    ]

    chain = (
        prompt
        | llm
        | parser
    )

    response = chain.invoke(
        {
            "history": conversation_history,
            "context": context,
            "question": question,
            "format_instructions": parser.get_format_instructions()
        }
    )

    conversation_history.append(
        {
            "user": question,
            "assistant": response
        }
    )

    response["source_metadata"] = source_metadata

    return response